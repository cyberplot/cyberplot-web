from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

@api.route("/hello/<string:name>/")
def say_hello(name):
    response = { "msg": "Hello {}".format(name) }
    return jsonify(response)