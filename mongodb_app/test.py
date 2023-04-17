import unittest

from app import app  # Import the Flask app to be tested


class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the Flask app context and a test client
            * ctx: The app context
            * client: The client that will be used to make requests
        """
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """
        Remove the app context after the test is complete
        """
        self.ctx.pop()

    def test_index(self):
        """
        Send a POST request to the /index route with some data, and follow the redirect
        Send a GET request to the /index route with the same data in the query string
            * response: The response from the request
            * data: The data that will be sent in the request
        """
        response = self.client.post(
            '/index',
            data=dict(content='go walking', degree='important'),
            follow_redirects=True
        )
        
        # Send a GET request to the /index route with the same data in the query string
        assert self.client.get('/index', query_string=dict(content='go walking', degree='important'))

if __name__ == "__main__":
    unittest.main()  # Run the test suite if this file is being run directly
