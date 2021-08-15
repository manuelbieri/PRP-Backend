import unittest
import os.path

import customExceptions.Exceptions
import users.userHandler


class TestUsers(unittest.TestCase):
    path = os.path.dirname(__file__)

    @classmethod
    def setUpClass(cls) -> None:
        set_up_handler = users.userHandler.UserHandler(path=TestUsers.path)
        set_up_handler._createUserTable()
        set_up_handler.closeHandler()

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(TestUsers.path + "/users.db")

    def setUp(self) -> None:
        self.users = users.userHandler.UserHandler(path=TestUsers.path)
        self.setUpTestUser()

    def tearDown(self) -> None:
        self.users.closeHandler()

    def setUpTestUser(self):
        self.users.addUser("test", "validPassword")

    def test_valid_password(self):
        result: bool = self.users.checkPassword("test", "validPassword")
        self.assertTrue(result)

    def test_invalid_password(self):
        result: bool = self.users.checkPassword("test", "invalidPassword")
        self.assertFalse(result)

    def test_add_user(self):
        self.users.addUser('newUser', 'newPassword')
        result: bool = self.users.checkPassword("newUser", "newPassword")
        self.assertTrue(result)

    def test_add_invalid_password(self):
        self.assertRaises(AssertionError, self.users.addUser, 'user', 'short')

    def test_get_valid_user_id(self):
        user_id: int = self.users.getUserId('test')
        self.assertEqual(1, user_id)

    def test_get_invalid_user_id(self):
        self.assertRaises(customExceptions.Exceptions.InvalidUser, self.users.getUserId, 'invalid_username')
