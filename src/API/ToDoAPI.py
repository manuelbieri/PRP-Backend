import sqlite3
from typing import List

import flask
import flask_jwt_extended
import flask_restful

import API.APIUtilities
import customExceptions.Exceptions
import database.IDatabase as IdB
import database.ToDoDatabase as dB

data: IdB.IDatabase = dB.ToDoDatabase('todo.db', 'items')


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
