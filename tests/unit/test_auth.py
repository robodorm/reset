import unittest

from resetapp.auth import auth


class TestAuth(unittest.TestCase):

    def test_login_test(self):
        self.assertTrue(auth("test", "test") == 1)

    def test_login_user(self):
        self.assertTrue(auth("user", "user") == 2)

    def test_login_admin(self):
        self.assertTrue(auth("admin", "admin") == 3)

    def test_login_unknown(self):
        self.assertTrue(auth("__unknown__", "__unknown__") is None)


if __name__ == '__main__':
    unittest.main()
