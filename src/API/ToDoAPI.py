import sqlite3
import flask
import flask_jwt_extended
import flask_restful
from typing import List

import customExceptions.Exceptions
import database.ToDoDatabase as dB
import database.IDatabase as IdB

import API.APIUtilities
import users.JWTHandler as JWTHandler

app: flask.app.Flask = flask.Flask(__name__)
api: flask_restful.Api = flask_restful.Api(app, '/api/v1')
data: IdB.IDatabase = dB.ToDoDatabase('todo.db', 'items')
jwt: JWTHandler.JWTHandler = JWTHandler.JWTHandler(app)


class AllItems(flask_restful.Resource):
    @staticmethod
    @flask_jwt_extended.jwt_required()
    def get() -> flask.Response:
        entries: List[dict] = data.readAllEntries()
        return flask.jsonify(entries)


class SelectedItems(flask_restful.Resource):
    @staticmethod
    @flask_jwt_extended.jwt_required()
    def get() -> flask.Response:
        key: str = flask.request.args.get('key', type=str)
        value: str = flask.request.args.get('value', type=str)
        try:
            entries: List[dict] = data.readEntries(key, value)
        except sqlite3.OperationalError:
            return flask.jsonify({'type': 'exception', 'message': 'Database Error'})
        return flask.jsonify(entries)


class SingleItem(flask_restful.Resource):
    @staticmethod
    @flask_jwt_extended.jwt_required()
    def get() -> flask.Response:
        key: str = flask.request.args.get('key', type=str)
        value: str = flask.request.args.get('value', type=str)
        try:
            entry: dict = data.readEntry(key, value)
        except sqlite3.OperationalError:
            return flask.jsonify({'type': 'exception', 'message': 'Database Error'})
        return flask.jsonify(entry)

    @staticmethod
    @flask_jwt_extended.jwt_required()
    def post() -> flask.Response:
        title: str = flask.request.args.get('title', type=str)
        description: str = flask.request.args.get('description', type=str)
        try:
            API.APIUtilities.checkAPIArgs(title, description)
        except customExceptions.Exceptions.InvalidArgument:
            return flask.jsonify({'type': 'exception', 'message': 'Invalid Argument for this operation'})
        data.writeNewEntry({'title': title, 'description': description})
        return flask.jsonify({'type': 'success', 'message': 'Entry added successfully'})

    @staticmethod
    @flask_jwt_extended.jwt_required()
    def put() -> flask.Response:
        entry_id: int = flask.request.args.get('id', type=int)
        title: str = flask.request.args.get('title', type=str)
        description: str = flask.request.args.get('description', type=str)
        try:
            API.APIUtilities.checkAPIArgs(entry_id, title, description)
            API.APIUtilities.checkDatabaseID(entry_id)
        except customExceptions.Exceptions.InvalidArgument:
            return flask.jsonify({'type': 'exception', 'message': 'Invalid Argument for this operation'})
        data.updateEntry(entry_id, {'title': title, 'description': description})
        return flask.jsonify({'type': 'success', 'message': 'Entry deleted successfully'})

    @staticmethod
    @flask_jwt_extended.jwt_required()
    def delete() -> flask.Response:
        entry_id: int = flask.request.args.get('id', type=int)
        try:
            API.APIUtilities.checkDatabaseID(entry_id)
        except customExceptions.Exceptions.InvalidArgument:
            return flask.jsonify({'type': 'exception', 'message': 'Invalid Argument for this operation'})
        data.deleteEntry(entry_id)
        return flask.jsonify({'type': 'success', 'message': 'Entry deleted successfully'})


class APILogin(flask_restful.Resource):
    @staticmethod
    def post() -> flask.Response:
        username: str = flask.request.args.get('username', type=str)
        password: str = flask.request.args.get('password', type=str)
        try:
            response: flask.Response = flask.jsonify(jwt.login(username, password))
        except customExceptions.Exceptions.AuthenticationFailed as authFailed:
            response: flask.Response = flask.jsonify({'message': authFailed.__str__()})
        return response


class User(flask_restful.Resource):
    @staticmethod
    @flask_jwt_extended.jwt_required()
    def get():
        return flask.jsonify(flask_jwt_extended.get_jwt_identity())


api.add_resource(AllItems, '/todos/index')
api.add_resource(SelectedItems, '/todos')
api.add_resource(SingleItem, '/todo')
api.add_resource(APILogin, '/login')
api.add_resource(User, '/user')

if __name__ == "__main__":
    app.run(port=5001)
