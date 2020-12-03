from unittest import TestCase
from server import app
from model import connect_to_db, db
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Welcome", result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/handle-login",
                                  data={"email": "1@1.com", "password": "password1"},
                                  follow_redirects=True)
        self.assertIn(b"My Contacts", result.data)



class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['email'] = '1@1.com'

    def test_add_friend_page(self):
        """Test add friend page."""

        result = self.client.get("/add-a-friend")
        self.assertIn(b"Add a Friend", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_important_page(self):
        """Test that user can't see important page when logged out."""

        result = self.client.get("/add-a-friend", follow_redirects=True)
        self.assertNotIn(b"Add a Friend", result.data)
        self.assertIn(b"Sign In", result.data)




if __name__ == "__main__":
    import unittest

    unittest.main()
