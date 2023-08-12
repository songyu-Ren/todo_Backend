import unittest
from app import create_app, db
from app.services.todo_service import ToDoService
from app.models import ToDo
from . import BaseTestCase  # Import BaseTestCase from tests/__init__.py

class TestToDoService(BaseTestCase):
    

    def test_get_all_todos(self):
        # Setup
        todo1 = ToDo(content="Sample 1")
        todo2 = ToDo(content="Sample 2")
        db.session.add_all([todo1, todo2])
        db.session.commit()

        # Action
        todos = ToDoService.get_all_todos()

        # Assertion
        self.assertEqual(len(todos), 3) # one test todo created in the setUp method in ./__init__.py

    def test_get_completed_todos(self):
        # Setup
        todo1 = ToDo(content="Sample 1", is_completed=True)
        todo2 = ToDo(content="Sample 2", is_completed=False)
        db.session.add_all([todo1, todo2])
        db.session.commit()

        # Action
        todos = ToDoService.get_completed_todos()

        # Assertion
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].content, "Sample 1")

    def test_get_deleted_todos(self):
        # Setup
        todo1 = ToDo(content="Sample 1", is_deleted=True)
        todo2 = ToDo(content="Sample 2", is_deleted=False)
        db.session.add_all([todo1, todo2])
        db.session.commit()

        # Action
        todos = ToDoService.get_deleted_todos()

        # Assertion
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].content, "Sample 1")

    def test_create_todo(self):
        # Action
        todo_data = {"content": "New Task"}
        todo = ToDoService.create_todo(todo_data)  # Pass a dictionary

        # Assertion
        self.assertIsNotNone(todo.id)
        self.assertEqual(todo.content, "New Task")

    def test_update_todo(self):
        # Setup
        todo = ToDo(content="Original Task")
        db.session.add(todo)
        db.session.commit()

        # Action
        updated_todo = ToDoService.update_todo(todo.id, {"content": "Updated Task", "is_completed": True})

        # Assertion
        self.assertEqual(updated_todo.content, "Updated Task")
        self.assertTrue(updated_todo.is_completed)

    def test_delete_todo(self):
        # Setup
        todo = ToDo(content="Delete me")
        db.session.add(todo)
        db.session.commit()

        # Action
        result = ToDoService.delete_todo(todo.id)

        # Assertion
        self.assertTrue(result)
        deleted_todo = ToDo.query.get(todo.id)
        self.assertTrue(deleted_todo.is_deleted)

if __name__ == '__main__':
    unittest.main()
