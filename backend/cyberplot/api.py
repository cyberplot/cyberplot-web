from flask import Blueprint, jsonify, request
from .models import db, User, Dataset, Space, Attribute, Connector, DatasetVersion, Statistics
import simplejson as json

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
    attributes = Attribute.query.filter_by(uid = uid, did = did)
    statistics = Statistics.query.filter_by(uid = uid, did = did)
    return jsonify({ 'dataset': dataset,
                     'attributes': [a.to_dict() for a in attributes],
                     'statistics': [s.to_dict() for s in statistics] })

# Returns 5 results (UID, username) from User that match provided query
@api.route("/user_autocomplete/<string:phrase>/")
def userAutocomplete(phrase):
    users = User.query.filter(User.username.startswith(phrase)).limit(5).with_entities(User.uid, User.username)
    return jsonify({ 'users': [u for u in users] })