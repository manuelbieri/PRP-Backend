import flask
import flask_jwt_extended as jwt
import uuid

import customExceptions.Exceptions
import users.userHandler as userDB


class JWTHandler:
    def __init__(self, app: flask.app.Flask):
        self.app = app
        self.setSecretKey()
        self.JWTManager = jwt.JWTManager(app)
        self.users = userDB.UserHandler()

    def login(self, username: str, password: str) -> str:
        try:
            if self.users.checkPassword(username=username, password=password):
                user_id: int = self.users.getUserId(username)
                with self.app.app_context():
                    return jwt.create_access_token(identity=user_id)
            else:
                raise customExceptions.Exceptions.AuthenticationFailed('Invalid credentials')
        except TypeError:
            raise customExceptions.Exceptions.AuthenticationFailed('Invalid user')

    def setSecretKey(self):
        self.app.config['JWT_SECRET_KEY'] = str(uuid.uuid4())
