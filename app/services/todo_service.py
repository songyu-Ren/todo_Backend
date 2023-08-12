from app import db
from app.models import ToDo

class ToDoService:

    #create share function get list
    @staticmethod
    def get_list(is_completed=None, is_deleted=None):
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
        return ToDoService.get_list(is_deleted=False)

    #get all completed todo list method
    @staticmethod
    def get_completed_todos():
        return ToDoService.get_list(is_completed=True, is_deleted=False)

    #get all deleted todo list method
    @staticmethod
    def get_deleted_todos():
        return ToDoService.get_list(is_deleted=True)

    @staticmethod
    def create_todo(data):
        content_value = data.get('content')  
        if not content_value:
            return None
        todo = ToDo(content=content_value)
        db.session.add(todo)
        db.session.commit()
        return todo

    @staticmethod
    def update_todo(id, data):
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
        todo = ToDo.query.get(id)
        if not todo:
            return False
        todo.is_deleted = True
        db.session.commit()
        return True
