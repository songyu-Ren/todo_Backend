import unittest
from flask import json
from app import create_app, db
from app.models import ToDo
from unittest.mock import patch, Mock
from sqlalchemy.exc import OperationalError
from . import BaseTestCase  # Import BaseTestCase from tests/__init__.py

class TestToDoRoutes(BaseTestCase):

    # Test the root/home route
    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the ToDo API!", response.data)
    
    # Test retrieval of all ToDo items
    def test_get_all_todos_route(self):
        response = self.client.get('/todos')
        self.assertEqual(response.status_code, 200)

    # Test retrieval of completed ToDo items
    def test_get_completed_todos_route(self):
        todo = ToDo(content="Sample", is_completed=True)
        db.session.add(todo)
        db.session.commit()

        response = self.client.get('/todos/completed')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    # Test the creation of a ToDo item
    def test_create_todo_route(self):
        post_data = {
            "content": "Create this task"
        }
        response = self.client.post('/todos', json=post_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['content'], post_data["content"])

    # Test the update functionality of a ToDo item
    def test_update_todo_route(self):

        # Create an initial todo
        todo = ToDo(content="Original task")
        db.session.add(todo)
        db.session.commit()

        # Data to update the todo with
        put_data = {
            "content": "Updated task"
        }
        response = self.client.put(f'/todos/{todo.id}', json=put_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['content'], put_data["content"])

    # Test the delete (or mark as deleted) functionality of a ToDo item
    def test_delete_todo_route(self):
        todo = ToDo(content="Delete me")
        db.session.add(todo)
        db.session.commit()

        response = self.client.delete(f'/todos/{todo.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Todo marked as deleted', data['message'])

    # Test validation of ToDo input data
    def test_todo_input_validation(self):
        # Testing invalid content type
        invalid_data = {
            "content": 12345,  # Not a string
            "is_completed": True
        }
        response = self.client.post('/todos', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Content must be a string", response.get_json()["error"])

        # Testing invalid is_completed
        invalid_data = {
            "content": "Test Task",
            "is_completed": "yes"  # Not a boolean
        }
        response = self.client.post('/todos', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("is_completed must be a boolean", response.get_json()["error"])

    # Test for error handlers when a database error occurs
    @patch('app.models.ToDo.query')
    def test_database_error_handler(self, mock_query):
        # Mock the filter_by() method to raise a database OperationalError
        mock_query.filter_by.side_effect = OperationalError("statement", "params", "orig")
        response = self.client.get('/todos')
        self.assertEqual(response.status_code, 500) 
        self.assertIn("Database error occurred", response.get_json()["error"])

    # Test for error handlers when a resource is not found
    def test_not_found_error_handler(self):
        # Testing a non-existing todo
        response = self.client.get('/todos/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Resource not found", response.get_json()["error"])

# Run the tests
if __name__ == '__main__':
    unittest.main()
