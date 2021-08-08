import sqlite3

import flask
import flask_restful
from typing import List

import database.ToDoDatabase as dB

app = flask.Flask(__name__)
api = flask_restful.Api(app)
data = dB.ToDoDatabase('todo.db', 'items')


class AllItems(flask_restful.Resource):
    def get(self) -> flask.Response:
        entries: List[dict] = data.readAllEntries()
        return flask.jsonify(entries)


class SelectedItems(flask_restful.Resource):
    def get(self) -> flask.Response:
        key: str = flask.request.args.get('key', type=str)
        value: str = flask.request.args.get('value', type=str)
        try:
            entries: List[dict] = data.readEntries(key, value)
        except sqlite3.OperationalError:
            return flask.jsonify({'message': 'Database Error'})
        return flask.jsonify(entries)


class SingleItem(flask_restful.Resource):
    def get(self) -> flask.Response:
        key: str = flask.request.args.get('key', type=str)
        value: str = flask.request.args.get('value', type=str)
        try:
            entry: dict = data.readEntry(key, value)
        except sqlite3.OperationalError:
            return flask.jsonify({'message': 'Database Error'})
        return flask.jsonify(entry)


api.add_resource(AllItems, '/items/index')
api.add_resource(SelectedItems, '/items')
api.add_resource(SingleItem, '/item')

if __name__ == "__main__":
    app.run()
