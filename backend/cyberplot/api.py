from flask import Blueprint, jsonify, request
from .models import db, User, Dataset, Space, Attribute, DatasetConnector, UserConnector, DatasetVersion, Statistics
from .config import BaseConfig
from .utils import isValidCSV, getDatasetData
import simplejson as json
import csv, itertools, ast, werkzeug, os, datetime, secrets
from functools import wraps
import jwt

api = Blueprint("api", __name__)

def tokenRequired(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        authHeaders = request.headers.get("Authorization", "").split()

        if len(authHeaders) != 2:
            jsonify({'result': 'Authentication required.'}), 401

        try:
            token = authHeaders[1]
            data = jwt.decode(token, BaseConfig.SECRET_KEY)
            user = User.query.filter_by(username = data["sub"]).first()
            if not user:
                raise RuntimeError("User not found")
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            jsonify({'result': 'Authentication token expired.'}), 401
        except jwt.InvalidTokenError:
            jsonify({'result': 'Authentication required.'}), 401

    return _verify

# Returns metadata on all datasets belonging to user
@api.route("/dataset_list/")
@tokenRequired
def datasetList(user):
    datasets = Dataset.query.filter_by(uid = user.uid, deleted = False)
    return jsonify({ 'datasets': [d.to_dict() for d in datasets] })

# GET: Returns metadata on specified dataset along with attributes and their stats
# PUT: Allows for modification of dataset metadata
@api.route("/dataset/<int:did>/", methods = ("GET", "PUT",))
@tokenRequired
def dataset(user, did):
    if request.method == "GET":
        dataset = Dataset.query.filter_by(uid = user.uid, did = did, deleted = False).first().to_dict()

        lastVersion = DatasetVersion.query.filter_by(did = did).order_by(DatasetVersion.vid.desc()).first().to_dict()
        dataset["itemCount"] = lastVersion["itemCount"]
        filename = lastVersion["filename"]

        attributes_original = Attribute.query.filter_by(uid = user.uid, did = did)
        attributes = []

        for attribute in attributes_original:
            new_attribute = attribute.to_dict()
            new_attribute["values"] = []
            attributes.append(new_attribute)

        with open(filename) as csvfile:    
            reader = csv.reader(csvfile)
            for i, row in enumerate(itertools.islice(reader, BaseConfig.API_ATTRIBUTE_VALUE_PREVIEW_LENGTH + 1)):
                if i == 0:
                    continue # ignore the header
                for y, column in enumerate(row):
                    attributes[y]["values"].append(column)

        statistics = Statistics.query.filter_by(uid = user.uid, did = did)

        return jsonify({ 'dataset': dataset,
                        'attributes': attributes,
                        'statistics': [s.to_dict() for s in statistics] })

    elif request.method == "PUT":
        datasetChanged = False
        data = request.get_json()

        proposedName = data["dataset"]["name"]
        dataset = Dataset.query.filter_by(uid = user.uid, did = did).first()
        if proposedName != dataset.name:
            # check if another dataset does not have the same name
            if Dataset.query.filter_by(name = proposedName).first():
                return jsonify({'result': 'A dataset with specified name already exists.'}), 406

            dataset.name = data["dataset"]["name"]
            datasetChanged = True

        attributes = Attribute.query.filter_by(uid = user.uid, did = did)
        for i, attribute in enumerate(attributes):
            if data["attributes"][i]["label"] != attribute.label:
                proposedLabel = data["attributes"][i]["label"]
                # check if dataset does not include an attribute with the same label
                if Attribute.query.filter_by(label = proposedLabel).first():
                    return jsonify({'result': 'Dataset already contains an attribute with specified label.'}), 406

                attribute.label = data["attributes"][i]["label"]
                datasetChanged = True

        if datasetChanged:
            dataset.last_edit = datetime.datetime.now()
            db.session.commit()

        return jsonify({'result': True}), 201

# Returns 5 results (UID, username) from User that match provided query
@api.route("/user_autocomplete/<string:phrase>/")
@tokenRequired
def userAutocomplete(user, phrase):
    users = User.query.filter(User.username.startswith(phrase)).limit(5).with_entities(User.uid, User.username)
    return jsonify({ 'users': [u for u in users] })

# Used to create a new dataset or update an existing one
@api.route("/upload/", methods = ("POST",))
def uploadDataset():
    RequestForm = request.form
    data = RequestForm.to_dict(flat = False)
    metadata = str(data["json"][0])
    metadataDictionary = ast.literal_eval(metadata)["json"]

    createDataset = False
    apiKey = metadataDictionary["identifier"]
    connector = DatasetConnector.query.filter_by(key = apiKey).first()

    # if API key isn't associated with an existing dataset, 
    # presume we are creating a new table and look for user's API key
    if not connector: 
        connector = UserConnector.query.filter_by(key = apiKey).first()
        createDataset = True

        # if it's not there either, give up
        if not connector:
            return jsonify({'result': 'Provided API key is not valid.'}), 406

    userID = connector.to_dict()["UID"]
    datasetID = 0
    
    if createDataset:
        lastDataset = Dataset.query.filter_by(uid = userID).order_by(Dataset.did.desc()).first()
        if not lastDataset:
            datasetID = 1
        else:
            datasetID = lastDataset.to_dict()["DID"] + 1
    else:
        datasetID = connector.to_dict()["DID"]

    filename = "datasets/" + str(userID) + "/" + str(datasetID) + "/data.csv"

    # save file
    datasetData = request.files["file"]
    os.makedirs(os.path.dirname(filename), exist_ok = True)
    datasetData.save(filename)

    if not isValidCSV(filename):
        os.unlink(filename)
        return jsonify({'result': 'Provided file is not a valid CSV file.'}), 406

    if createDataset:
        datasetName = metadataDictionary["name"]
        if not datasetName:
            os.unlink(filename)
            return jsonify({'result': 'Please provide a dataset name.'}), 406

        # do not allow the user to have two datasets with same name
        if Dataset.query.filter_by(name = metadataDictionary["name"], uid = userID).first():
            os.unlink(filename)
            return jsonify({'result': 'Dataset with specified name already exists.'}), 406

        # get file data, attributes, item count, statistics
        datasetData = getDatasetData(filename)

        newDataset = Dataset(uid = userID,
                             did = datasetID,
                             name = datasetName,
                             last_edit = datetime.datetime.now(),
                             deleted = False)
        db.session.add(newDataset)

        newDatasetVersion = DatasetVersion(vid = 1,
                                           uid = userID,
                                           did = datasetID,
                                           filename = filename,
                                           upload_date = datetime.datetime.now(),
                                           item_count = datasetData["itemCount"])
        db.session.add(newDatasetVersion)

        for i, attribute in enumerate(datasetData["attributes"]):
            attribute.uid = userID
            attribute.did = datasetID
            attribute.aid = i + 1 # SQL increments from 1
            attribute.missing_value_setting = 0
            db.session.add(attribute)

        for statistics in datasetData["statistics"]:
            statistics.uid = userID
            statistics.did = datasetID
            db.session.add(statistics)
        
        # generate API key for dataset
        while True:
            key = secrets.token_hex(nbytes = 16)

            # make sure we generate a unique key
            if not DatasetConnector.query.filter_by(key = key).first():
                if not UserConnector.query.filter_by(key = key).first():
                    connector = DatasetConnector(uid = userID, did = datasetID, key = key)
                    db.session.add(connector)
                    break

        db.session.commit()

    else:
        print("update") #TODO
        datasetData = getDatasetData(filename)

    return jsonify({'result': True}), 201

# deletes dataset files and all metadata associated with it
@api.route("/dataset_delete/<int:did>/", methods = ("POST",))
@tokenRequired
def deleteDataset(user, did):
    datasetVersions = DatasetVersion.query.filter_by(uid = user.uid, did = did)
    for version in datasetVersions:
        os.unlink(version.filename)

    Space.query.filter_by(dataset_uid = user.uid, did = did).delete()
    Statistics.query.filter_by(uid = user.uid, did = did).delete()
    Attribute.query.filter_by(uid = user.uid, did = did).delete()
    DatasetVersion.query.filter_by(uid = user.uid, did = did).delete()
    DatasetConnector.query.filter_by(uid = user.uid, did = did).delete()
    Dataset.query.filter_by(uid = user.uid, did = did).delete()
    db.session.commit()

    return jsonify({'result': True}), 201

# Get information about user that is logged in
@api.route("/user_info/")
@tokenRequired
def userInfo(user):
    return jsonify({'user': user.to_dict()})

@api.route("/signup/", methods = ("POST",))
def signup():
    data = request.get_json()
    user = User(**data)
    if User.query.filter_by(username = user.username).first():
        return jsonify({'result': 'Specified username is already taken.'}), 406

    user.account_type = 0
    db.session.add(user)

    userID = User.query.filter_by(username = user.username).first().uid

    while True:
        key = secrets.token_hex(nbytes = 16)

        # make sure we generate a unique key
        if not DatasetConnector.query.filter_by(key = key).first():
            if not UserConnector.query.filter_by(key = key).first():
                connector = UserConnector(uid = userID, key = key)
                db.session.add(connector)
                break

    db.session.commit()
    return jsonify({'result': True}), 201

@api.route("/login/", methods = ("POST",))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'result': 'Invalid username or password.'}), 401

    token = jwt.encode({'sub': user.username, 'iat': datetime.datetime.utcnow(), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, BaseConfig.SECRET_KEY)
    return jsonify({'token': token.decode('UTF-8')})