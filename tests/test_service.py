import unittest
from app import create_app, db
from app.services.todo_service import ToDoService
from app.models import ToDo
from . import BaseTestCase  # Import BaseTestCase from tests/__init__.py

class TestToDoService(BaseTestCase):
    
    # Test the retrieval of all todo items.
    def test_get_all_todos(self):

        # Setup: : Create and commit two test todos
        todo1 = ToDo(content="Sample 1")
        todo2 = ToDo(content="Sample 2")
        db.session.add_all([todo1, todo2])
        db.session.commit()

        # Action: Fetch all todos using the service
        todos = ToDoService.get_all_todos()

        # Assertion: Check the count and contents of retrieved todos
        self.assertEqual(len(todos), 3) # one test todo created in the setUp method in ./__init__.py
    
    #Test the retrieval of completed todo items.
    def test_get_completed_todos(self):

        # Setup: Create and commit two todos, one of which is completed
        todo1 = ToDo(content="Sample 1", is_completed=True)
        todo2 = ToDo(content="Sample 2", is_completed=False)
        db.session.add_all([todo1, todo2])
        db.session.commit()

        # Action: Fetch completed todos using the service
        todos = ToDoService.get_completed_todos()

        # Assertion: Check the count and contents of retrieved todos
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].content, "Sample 1")

    #Test the retrieval of deleted todo items.
    def test_get_deleted_todos(self):

        # Setup: Create and commit two todos, one of which is deleted
        todo1 = ToDo(content="Sample 1", is_deleted=True)
        todo2 = ToDo(content="Sample 2", is_deleted=False)
        db.session.add_all([todo1, todo2])
        db.session.commit()

        # Action: Fetch deleted todos using the service
        todos = ToDoService.get_deleted_todos()

        # Assertion: Check the count and contents of retrieved todos
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].content, "Sample 1")

    #Test the creation of a new todo item.
    def test_create_todo(self):

        # Action: Create a new todo using the service
        todo_data = {"content": "New Task"}
        todo = ToDoService.create_todo(todo_data)  # Pass a dictionary

        # Assertion: Verify the created todo's attributes
        self.assertIsNotNone(todo.id)
        self.assertEqual(todo.content, "New Task")

    #Test the update functionality of a todo item.
    def test_update_todo(self):

        # Setup: Create and commit a test todo
        todo = ToDo(content="Original Task")
        db.session.add(todo)
        db.session.commit()

        # Action: Update the todo using the service
        updated_todo = ToDoService.update_todo(todo.id, {"content": "Updated Task", "is_completed": True})

        # Assertion: Verify the updated attributes of the todo
        self.assertEqual(updated_todo.content, "Updated Task")
        self.assertTrue(updated_todo.is_completed)

    #Test the soft deletion of a todo item 
    # (marking it as deleted without actually removing it).
    def test_delete_todo(self):
        # Setup: Create and commit a test todo
        todo = ToDo(content="Delete me")
        db.session.add(todo)
        db.session.commit()

        # Action: Mark the todo as deleted using the service
        result = ToDoService.delete_todo(todo.id)

        # Assertion: Verify that the todo was marked as deleted
        self.assertTrue(result)
        deleted_todo = ToDo.query.get(todo.id)
        self.assertTrue(deleted_todo.is_deleted)

if __name__ == '__main__':
    unittest.main()
