import unittest
from app import create_app, db
from app.models import ToDo

class BaseTestCase(unittest.TestCase):
     # Code to set up the test environment, initializing the database
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        test_todo = ToDo(content="Test Todo")
        db.session.add(test_todo)
        db.session.commit()

    def tearDown(self):
        # Code to clean up after the test, e.g., deleting all database entries
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
