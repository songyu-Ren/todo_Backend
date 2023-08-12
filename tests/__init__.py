import unittest
from app import create_app, db
from app.models import ToDo

#Base Test Case for setting up and tearing down the test environment.  
class BaseTestCase(unittest.TestCase):

     # Code to set up the test environment before each test
    def setUp(self):

        # Create an instance of the app with testing configuration
        self.app = create_app('testing')
        # Get the test client for sending simulated HTTP requests
        self.client = self.app.test_client()
        # Create an app context to bind the application to the current context
        self.app_context = self.app.app_context()
        # Push the application context to ensure it's active for this test
        self.app_context.push()
        # Create all database tables required for testing
        db.create_all()

        # Add a sample ToDo to the database for testing
        test_todo = ToDo(content="Test Todo")
        db.session.add(test_todo)
        db.session.commit()

    # Code to clean up after each test
    def tearDown(self):
        # Remove the current database session
        db.session.remove()
        # Drop all tables from the database to ensure a clean state
        db.drop_all()
        # Pop the application context to revert back to the previous context
        self.app_context.pop()
