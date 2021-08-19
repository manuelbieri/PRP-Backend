import flask
import flask_jwt_extended
import flask_restful

import API.ToDoAPI
import API.APIUtilities
import users.JWTHandler as JWTHandler
import customExceptions.Exceptions as Exceptions

app: flask.app.Flask = flask.Flask(__name__)
api: flask_restful.Api = flask_restful.Api(app, '/api/v1')
jwt: JWTHandler.JWTHandler = JWTHandler.JWTHandler(app)


class APILogin(flask_restful.Resource):
    @staticmethod
    def post() -> flask.Response:
        username: str = flask.request.args.get('username', type=str)
        password: str = flask.request.args.get('password', type=str)
        try:
            response: flask.Response = flask.jsonify(jwt.login(username, password))
        except Exceptions.AuthenticationFailed as authFailed:
            response: flask.Response = flask.jsonify({'message': authFailed.__str__()})
        return response


class User(flask_restful.Resource):
    @staticmethod
    @flask_jwt_extended.jwt_required()
    def get():
        return flask.jsonify(flask_jwt_extended.get_jwt_identity())

class Test(flask_restful.Resource):
    @staticmethod
    def get():
        return flask.jsonify({'message': 'success'})

api.add_resource(API.ToDoAPI.AllItems, '/todo/index')
api.add_resource(API.ToDoAPI.SelectedItems, '/todo')
api.add_resource(API.ToDoAPI.SingleItem, '/todo')
api.add_resource(APILogin, '/login')
api.add_resource(User, '/user')
api.add_resource(Test, '/')

if __name__ == "__main__":
    app.run(port=5001)
