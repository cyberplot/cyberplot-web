from flask import Blueprint, jsonify, request
from .models import db, User, Dataset, Space, Attribute, DatasetConnector, UserConnector, DatasetVersion, Statistics
from .config import BaseConfig
import simplejson as json
import csv, itertools

api = Blueprint("api", __name__)

# Returns metadata on all datasets belonging to user
@api.route("/dataset_list/<int:uid>/")
def datasetList(uid):
    datasets = Dataset.query.filter_by(uid = uid, deleted = False)
    return jsonify({ 'datasets': [d.to_dict() for d in datasets] })

# Returns metadata on specified dataset along with attributes and their stats
@api.route("/dataset/<int:uid>/<int:did>/")
def dataset(uid, did):
    dataset = Dataset.query.filter_by(uid = uid, did = did, deleted = False).first().to_dict()
    dataset["item_count"] = DatasetVersion.query.filter_by(did = did).order_by(DatasetVersion.vid.desc()).first().to_dict()["itemCount"]

    attributes_original = Attribute.query.filter_by(uid = uid, did = did)
    attributes = []

    for attribute in attributes_original:
        new_attribute = attribute.to_dict()
        new_attribute["values"] = []
        attributes.append(new_attribute)

    with open('migrations/iris.csv') as csvfile:    
        reader = csv.reader(csvfile)
        for i, row in enumerate(itertools.islice(reader, BaseConfig.API_ATTRIBUTE_VALUE_PREVIEW_LENGTH + 1)):
            if i == 0:
                continue # ignore the header
            for y, column in enumerate(row):
                attributes[y]["values"].append(column)

    statistics = Statistics.query.filter_by(uid = uid, did = did)

    return jsonify({ 'dataset': dataset,
                     'attributes': attributes,
                     'statistics': [s.to_dict() for s in statistics] })

# Returns 5 results (UID, username) from User that match provided query
@api.route("/user_autocomplete/<string:phrase>/")
def userAutocomplete(phrase):
    users = User.query.filter(User.username.startswith(phrase)).limit(5).with_entities(User.uid, User.username)
    return jsonify({ 'users': [u for u in users] })