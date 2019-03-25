#!/usr/bin/env python3
# coding=utf-8
import string
from random import choices

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token
)
from flask_rest_jsonapi import Api

from resetapp.auth import auth
from resetapp.rest_schemes.todo.task_schema import TaskList, TaskDetail
from resetapp.settings import CACHE_EXPIRES, CACHE_CONTROL

""" # APP CORE CONFIGURATION #
"""

app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join(choices(string.ascii_uppercase + string.digits, k=21))

jwt = JWTManager(app)

# Please configure this part according to your needs
# Current solution is not for production environment
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.after_request
def add_header(response):
    response.cache_control.max_age = CACHE_EXPIRES

    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = CACHE_CONTROL

    return response


""" # START SYSTEM ENDPOINTS #
"""


@app.route("/ping")
def ping():
    return "pong"


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    identity = auth(username, password)
    if not identity:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity={"uid": identity})
    return jsonify(access_token=access_token), 200


@app.route("/")
def main():
    return "ok"


""" # START VERSIONED API ENDPOINTS #
"""

api = Api(app)

# todo: move to the admin page possibility to enable or disable modules
AVAILABLE_ACTIONS = [TaskList, TaskDetail, ]

for action in AVAILABLE_ACTIONS:
    api.route(action, action.rest_desc(), action.route())

if __name__ == '__main__':
    app.run(debug=True, host="0.0", port=80)
