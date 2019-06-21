from flask import Blueprint, jsonify, request, send_file
from .models import db, User, Dataset, Space, Attribute, DatasetConnector, UserConnector, DatasetVersion, Statistics, ShareRequest
from .config import BaseConfig
from .utils import isValidCSV, getDatasetData, isFlagOnPosition, typeToInt, attributeTypes, getDatasetFilepath
import simplejson as json
import csv, itertools, ast, werkzeug, os, datetime, secrets
from functools import wraps
import jwt
from email.utils import parseaddr
from shutil import copyfile

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
            return jsonify({'result': 'Authentication token expired.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'result': 'Authentication required.'}), 401

    return _verify

# Returns metadata on all datasets belonging to user
@api.route("/dataset_list/")
@tokenRequired
def datasetList(user):
    datasets = Dataset.query.filter_by(uid = user.uid, deleted = False).order_by(Dataset.last_edit.desc())
    return jsonify({ 'datasets': [d.to_dict() for d in datasets] })

# GET: Returns metadata on specified dataset along with attributes and their stats
# PUT: Allows for modification of dataset metadata
@api.route("/dataset/<int:did>/", methods = ("GET", "PUT",))
@tokenRequired
def dataset(user, did):
    if request.method == "GET":
        dataset = Dataset.query.filter_by(uid = user.uid, did = did, deleted = False).first().to_dict()
        datasetVersions = DatasetVersion.query.filter_by(uid = user.uid, did = did).order_by(DatasetVersion.vid.desc())

        lastVersion = DatasetVersion.query.filter_by(did = did).order_by(DatasetVersion.vid.desc()).first()
        dataset["itemCount"] = lastVersion.to_dict()["itemCount"]
        filepath = lastVersion.filepath()

        attributes_original = Attribute.query.filter_by(uid = user.uid, did = did)
        attributes = []

        for attribute in attributes_original:
            new_attribute = attribute.to_dict()
            new_attribute["values"] = []
            attributes.append(new_attribute)

        rowsToGet = BaseConfig.API_ATTRIBUTE_VALUE_PREVIEW_LENGTH
        if lastVersion.to_dict()["containsHeader"]:
            rowsToGet = rowsToGet + 1

        with open(filepath) as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(itertools.islice(reader, rowsToGet)):
                if i == 0 and lastVersion.to_dict()["containsHeader"]:
                    continue # ignore the header
                for y, column in enumerate(row):
                    attributes[y]["values"].append(column)

        statistics = Statistics.query.filter_by(uid = user.uid, did = did)
        key = DatasetConnector.query.filter_by(uid = user.uid, did = did).first().key

        return jsonify({ 'dataset': dataset,
                        'attributes': attributes,
                        'statistics': [s.to_dict() for s in statistics],
                        'datasetVersions': [v.to_dict() for v in datasetVersions],
                        'key': key })

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

        if len(proposedName) == 0:
            return jsonify({'result': 'Dataset name cannot be blank.'}), 406

        attributes = Attribute.query.filter_by(uid = user.uid, did = did)
        for i, attribute in enumerate(attributes):
            if data["attributes"][i]["label"] != attribute.label:
                proposedLabel = data["attributes"][i]["label"]
                # check if dataset does not include an attribute with the same label
                if Attribute.query.filter_by(label = proposedLabel).first():
                    return jsonify({'result': 'Dataset already contains an attribute with specified label.'}), 406

                if len(proposedLabel) == 0:
                    return jsonify({'result': 'Attribute label cannot be blank.'}), 406

                attribute.label = data["attributes"][i]["label"]
                datasetChanged = True
            
            try:
                proposedType = typeToInt(attributeTypes[data["attributes"][i]["type"].upper()])
                if proposedType != attribute.type:
                    if isFlagOnPosition(attribute.type_mask, proposedType):
                        attribute.type = proposedType
                        datasetChanged = True
                    else:
                        return jsonify({'result': 'Type is invalid for select attribute.'}), 406
            except KeyError:
                return jsonify({'result': 'Invalid attribute type given.'}), 406

        if data["dataset"]["versioningOn"] != dataset.versioning_on:
            if not dataset.versioning_on:
                dataset.versioning_on = True

            else:
                # remove all versions and associated files except for the last one
                versions = DatasetVersion.query.filter_by(uid = user.uid, did = did).order_by(DatasetVersion.vid.desc())
                for i, version in enumerate(versions):
                    if(i == 0): # do not remove the last version
                        continue
                    os.unlink(version.filepath())
                    DatasetVersion.query.filter_by(uid = user.uid, did = did, vid = version.vid).delete()

                dataset.versioning_on = False
            
            datasetChanged = True

        if datasetChanged:
            dataset.last_edit = datetime.datetime.now()
            db.session.commit()

        return jsonify({'result': True}), 201

# Returns 5 results (UID, username) from User that match provided query
@api.route("/user_autocomplete/<string:phrase>/")
@tokenRequired
def userAutocomplete(user, phrase):
    users = User.query.filter(User.username.startswith(phrase), User.username != user.username).limit(5).with_entities(User.uid, User.username)
    return jsonify({ 'users': [u for u in users] })

# Used to create a new dataset or update an existing one
@api.route("/dataset_upload/", methods = ("POST",))
def uploadDataset():
    RequestForm = request.form
    data = RequestForm.to_dict(flat = False)
    metadata = str(data["json"][0])
    metadataDictionary = ast.literal_eval(metadata)["json"]

    createDataset = False
    apiKey = metadataDictionary["identifier"]
    containsHeader = metadataDictionary["containsHeader"]
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


    versionNumber = 1
    if not createDataset:
        versionNumber = DatasetVersion.query.filter_by(uid = userID, did = datasetID).order_by(DatasetVersion.vid.desc()).first().vid

        if Dataset.query.filter_by(uid = userID, did = datasetID).first().versioning_on:
            versionNumber = versionNumber + 1

    filepath = getDatasetFilepath("data.csv", userID, datasetID, versionNumber)

    # save file
    datasetData = request.files["file"]
    os.makedirs(os.path.dirname(filepath), exist_ok = True)
    datasetData.save(filepath)

    if not isValidCSV(filepath):
        os.unlink(filepath)
        return jsonify({'result': 'Provided file is not a valid CSV file.'}), 406

    if createDataset:
        datasetName = metadataDictionary["name"]
        if not datasetName:
            os.unlink(filepath)
            return jsonify({'result': 'Please provide a dataset name.'}), 406

        # do not allow the user to have two datasets with same name
        if Dataset.query.filter_by(name = datasetName, uid = userID).first():
            appendedNumber = 1
            # increment number until we find one that is unused
            while Dataset.query.filter_by(name = datasetName + " (" + str(appendedNumber) + ")").first():
                appendedNumber = appendedNumber + 1
            
            datasetName = datasetName + " (" + str(appendedNumber) + ")"

        # get file data, attributes, item count, statistics
        datasetData = getDatasetData(filepath, containsHeader)

        newDataset = Dataset(uid = userID,
                             did = datasetID,
                             name = datasetName,
                             last_edit = datetime.datetime.now(),
                             deleted = False,
                             versioning_on = False)
        db.session.add(newDataset)

        newDatasetVersion = DatasetVersion(vid = 1,
                                           uid = userID,
                                           did = datasetID,
                                           filename = "data.csv",
                                           upload_date = datetime.datetime.now(),
                                           item_count = datasetData["itemCount"],
                                           contains_header = containsHeader)
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
        datasetData = getDatasetData(filepath, containsHeader)
        dataset = Dataset.query.filter_by(uid = userID, did = datasetID).first()
        dataset.last_edit = datetime.datetime.now()

        if dataset.versioning_on:
            newDatasetVersion = DatasetVersion(vid = versionNumber,
                                               uid = userID,
                                               did = datasetID,
                                               filename = "data.csv",
                                               upload_date = datetime.datetime.now(),
                                               item_count = datasetData["itemCount"],
                                               contains_header = containsHeader)
            db.session.add(newDatasetVersion)

        else:
            datasetVersion = DatasetVersion.query.filter_by(uid = userID, did = datasetID).first()
            datasetVersion.filename = "data.csv"
            datasetVersion.upload_date = datetime.datetime.now()
            datasetVersion.item_count = datasetData["itemCount"]
            datasetVersion.containsHeader = containsHeader

        if Attribute.query.filter_by(uid = userID, did = datasetID).count() != len(datasetData["attributes"]):
            os.unlink(filepath)
            return jsonify({'result': 'Number of attributes does not match the original dataset.'}), 406

        for i, newAttribute in enumerate(datasetData["attributes"]):
            attribute = Attribute.query.filter_by(uid = userID, did = datasetID, aid = i + 1).first()
            if newAttribute.type_mask != attribute.type_mask:
                os.unlink(filepath)
                return jsonify({'result': 'Attribute types do not match the original dataset.'}), 406

        statistics = Statistics.query.filter_by(uid = userID, did = datasetID).delete()
        for statistics in datasetData["statistics"]:
            statistics.uid = userID
            statistics.did = datasetID
            db.session.add(statistics)

        db.session.commit()

    return jsonify({'result': True}), 201

# deletes dataset files and all metadata associated with it
@api.route("/dataset_delete/<int:did>/", methods = ("POST",))
@tokenRequired
def deleteDataset(user, did):
    datasetVersions = DatasetVersion.query.filter_by(uid = user.uid, did = did)
    for version in datasetVersions:
        os.unlink(version.filepath())

    Space.query.filter_by(dataset_uid = user.uid, did = did).delete()
    Statistics.query.filter_by(uid = user.uid, did = did).delete()
    Attribute.query.filter_by(uid = user.uid, did = did).delete()
    DatasetVersion.query.filter_by(uid = user.uid, did = did).delete()
    DatasetConnector.query.filter_by(uid = user.uid, did = did).delete()
    ShareRequest.query.filter_by(uid_sender = user.uid, did = did).delete()
    Dataset.query.filter_by(uid = user.uid, did = did).delete()
    db.session.commit()

    return jsonify({'result': True}), 201

# deletes last dataset version nad associated file
@api.route("/dataset_version_delete/<int:did>/<int:vid>/", methods = ("POST",))
@tokenRequired
def deleteDatasetVersion(user, did, vid):
    version = DatasetVersion.query.filter_by(uid = user.uid, did = did, vid = vid).first()
    os.unlink(version.filepath())
    DatasetVersion.query.filter_by(uid = user.uid, did = did, vid = vid).delete()
    db.session.commit()

    return jsonify({'result': True}), 201

# Provides data file of last dataset version
@api.route("/dataset_download/<int:did>/")
@tokenRequired
def downloadDataset(user, did):
    path = DatasetVersion.query.filter_by(uid = user.uid, did = did).order_by(DatasetVersion.vid.desc()).first().filepath()
    return send_file(path, as_attachment = True)

# Provides data file of selected dataset version
@api.route("/dataset_version_download/<int:did>/<int:vid>/")
@tokenRequired
def downloadDatasetVersion(user, did, vid):
    path = DatasetVersion.query.filter_by(uid = user.uid, did = did, vid = vid).first().filepath()
    return send_file(path, as_attachment = True)

# Creates a share request to selected user
@api.route("/dataset_share/<int:did>/<int:uidReceiver>/", methods = ("POST",))
@tokenRequired
def shareDataset(user, did, uidReceiver):
    if user.uid == uidReceiver:
        return jsonify({'result': 'Dataset receiver must be different from sender.'})

    if not Dataset.query.filter_by(did = did, uid = user.uid).first():
        return jsonify({'result': 'Specified dataset does not exist.'}), 406
    
    if not User.query.filter_by(uid = uidReceiver).first():
        return jsonify({'result': 'Receiving user does not exist.'}), 406

    if ShareRequest.query.filter_by(did = did, uid_sender = user.uid, uid_receiver = uidReceiver).first():
        return jsonify({'result': 'Specified share request already exists.'}), 406

    newShareRequest = ShareRequest(did = did,
                                   uid_sender = user.uid,
                                   uid_receiver = uidReceiver,
                                   timestamp = datetime.datetime.now())
    db.session.add(newShareRequest)
    db.session.commit()

    return jsonify({'result': True}), 201

# Gets all pending share requests for user
@api.route("/share_requests/")
@tokenRequired
def shareRequests(user):
    requestsOriginal = ShareRequest.query.filter_by(uid_receiver = user.uid).order_by(ShareRequest.timestamp.desc())

    requests = []

    for request in requestsOriginal:
        newRequest = request.to_dict()
        newRequest["username"] = User.query.filter_by(uid = newRequest["UIDsender"]).first().to_dict()["username"]
        newRequest["datasetName"] = Dataset.query.filter_by(did = newRequest["DID"]).first().to_dict()["name"]
        requests.append(newRequest)

    return jsonify({ 'requests': requests })

@api.route("/share_request_answer/", methods = ("POST",))
@tokenRequired
def answerShareRequest(user):
    _request = request.get_json()["request"]
    originalRequest = ShareRequest.query.filter_by(did = _request["DID"], uid_sender = _request["UIDsender"], uid_receiver = _request["UIDreceiver"])

    if not originalRequest:
        return jsonify({'result': 'Specified request does not exist.'}), 406

    if _request["accepted"]:
        datasetCopyDID = 1
        if Dataset.query.filter_by(uid = user.uid).order_by(Dataset.did.desc()).first():
            datasetCopyDID = Dataset.query.filter_by(uid = user.uid).order_by(Dataset.did.desc()).first().to_dict()["DID"] + 1

        dataset = Dataset.query.filter_by(did = _request["DID"], uid = _request["UIDsender"]).first()
        dataset.uid = user.uid
        dataset.did = datasetCopyDID
        db.session.add(dataset)

        for attribute in Attribute.query.filter_by(did = _request["DID"], uid = _request["UIDsender"]):
            attribute.uid = user.uid
            attribute.did = datasetCopyDID
            db.session.add(attribute)
        
        for statistics in Attribute.query.filter_by(did = _request["DID"], uid = _request["UIDsender"]):
            statistics.uid = user.uid
            statistics.did = datasetCopyDID
            db.session.add(statistics)

        for version in DatasetVersion.query.filter_by(did = _request["DID"], uid = _request["UIDsender"]):
            oldFilepath = version.filepath()
            version.uid = user.uid
            version.did = datasetCopyDID
            os.makedirs(version.dirpath(), exist_ok = True)
            copyfile(oldFilepath, version.filepath())

        # generate API key for dataset
        #TODO DRY - reused from dataset_upload
        while True:
            key = secrets.token_hex(nbytes = 16)

            # make sure we generate a unique key
            if not DatasetConnector.query.filter_by(key = key).first():
                if not UserConnector.query.filter_by(key = key).first():
                    connector = DatasetConnector(uid = user.uid, did = datasetCopyDID, key = key)
                    db.session.add(connector)
                    break

    originalRequest.delete()
    db.session.commit()

    return jsonify({'result': True}), 201

# Get information about user that is logged in
@api.route("/user_info/")
@tokenRequired
def userInfo(user):
    key = UserConnector.query.filter_by(uid = user.uid).first().key
    return jsonify({'user': user.to_dict(), 'key': key})

@api.route("/signup/", methods = ("POST",))
def signup():
    data = request.get_json()
    user = User(**data)
    user.username = user.username.lower()
    if User.query.filter_by(username = user.username).first():
        return jsonify({'result': 'Specified username is already taken.'}), 406

    if not "@" in parseaddr(user.email)[1]:
        return jsonify({'result': 'E-mail address is not valid.'}), 406

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