from app import db
from app.models import ToDo

class ToDoService:

    #create share function get list
    @staticmethod
    def get_list(is_completed=None, is_deleted=None):
        """
        Retrieve a list of ToDo items based on the provided filters.

        Args:
            is_completed (bool, optional): Filter ToDo items by completion status.
            is_deleted (bool, optional): Filter ToDo items by deletion status.

        Returns:
            list: A list of ToDo items that match the filters.
        """
        # Handle the cases where is_completed and is_deleted are None
        filters = {}
        if is_completed is not None:
            filters["is_completed"] = is_completed
        if is_deleted is not None:
            filters["is_deleted"] = is_deleted

        return ToDo.query.filter_by(**filters).all()

    #get all todo list method
    @staticmethod
    def get_all_todos():
        """
        Retrieve all ToDo items that are not deleted.

        Returns:
            list: A list of non-deleted ToDo items.
        """
        return ToDoService.get_list(is_deleted=False)

    #get all completed todo list method
    @staticmethod
    def get_completed_todos():
        """
        Retrieve all completed ToDo items that are not deleted.

        Returns:
            list: A list of completed, non-deleted ToDo items.
        """
        return ToDoService.get_list(is_completed=True, is_deleted=False)

    #get all deleted todo list method
    @staticmethod
    def get_deleted_todos():
        """
        Retrieve all ToDo items that are marked as deleted.

        Returns:
            list: A list of deleted ToDo items.
        """
        return ToDoService.get_list(is_deleted=True)

    @staticmethod
    def create_todo(data):
        """
        Create a new ToDo item using the provided data.

        Args:
            data (dict): Dictionary containing data for the new ToDo item.
                         Expected to have a 'content' key.

        Returns:
            ToDo: The newly created ToDo item, or None if creation failed.
        """
        content_value = data.get('content')  
        if not content_value:
            return None
        todo = ToDo(content=content_value)
        db.session.add(todo)
        db.session.commit()
        return todo

    @staticmethod
    def update_todo(id, data):
        """
        Update an existing ToDo item using the provided data.

        Args:
            id (int): The ID of the ToDo item to update.
            data (dict): Dictionary containing the updated data for the ToDo item.

        Returns:
            ToDo: The updated ToDo item, or None if the item was not found.
        """
        todo = ToDo.query.get(id)
        if not todo:
            return None
        content = data.get('content')
        is_completed = data.get('is_completed')
        if content:
            todo.content = content
        if is_completed is not None:
            todo.is_completed = is_completed
        db.session.commit()
        return todo

    @staticmethod
    def delete_todo(id):
        """
        Soft delete a ToDo item by marking it as deleted.

        Args:
            id (int): The ID of the ToDo item to mark as deleted.

        Returns:
            bool: True if the item was successfully marked as deleted, False otherwise.
        """
        todo = ToDo.query.get(id)
        if not todo:
            return False
        todo.is_deleted = True
        db.session.commit()
        return True
