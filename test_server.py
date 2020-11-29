"""Sample test suite for testing demo."""

import server
import unittest


def load_tests(loader, tests, ignore):
    """Also run our doctests and file-based doctests.

    This function name, ``load_tests``, is required.
    """

    tests.addTests(doctest.DocTestSuite(arithmetic))
    tests.addTests(doctest.DocFileSuite("tests.txt"))
    return tests


class MyAppIntegrationTestCase(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""

    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn(b'<h1>Color Form</h1>', result.data)

    def test_favorite_color_form(self):
        client = server.app.test_client()
        result = client.post('/fav-color', data={'color': 'blue'})
        self.assertIn(b'Woah! I like blue, too', result.data)


class MyAppIntegrationTestCase2(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""

    def setUp(self):
        # print("(setUp ran)")
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        # We don't need to do anything here; we could just
        # not define this method at all, but we have a stub
        # here as an example.
        # print("(tearDown ran)")
        return

    def test_index(self):
        result = self.client.get('/')
        self.assertIn(b'<h1>Color Form</h1>', result.data)

    def test_favorite_color_form(self):
        result = self.client.post('/fav-color', data={'color': 'blue'})
        self.assertIn(b'Woah! I like blue, too', result.data)


if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
