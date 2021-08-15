import unittest

import flask

import customExceptions.Exceptions
import users.JWTHandler as JWTHandler


class JWTTest(unittest.TestCase):
    def setUp(self) -> None:
        self.jwt: JWTHandler.JWTHandler = JWTHandler.JWTHandler(flask.Flask(__name__))

    def test_valid_login(self):
        response = self.jwt.login('admin', 'adminTest')
        self.assertNotEqual(None, response)

    def test_invalid_username_login(self):
        self.assertRaises(customExceptions.Exceptions.AuthenticationFailed, self.jwt.login, 'invalid', 'adminTest')

    def test_invalid_password_login(self):
        self.assertRaises(customExceptions.Exceptions.AuthenticationFailed, self.jwt.login, 'admin', 'invalid_password')
