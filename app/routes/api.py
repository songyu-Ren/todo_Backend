from flask import jsonify, request, Blueprint 
from app import create_app, db
from app.models import ToDo, Importance
from app.services import ToDoService
from sqlalchemy.exc import DatabaseError

api = Blueprint('api', __name__)

# Helper function to validate input
def validate_todo_input(data):
    if not data:
        raise ValueError("No data provided.")

    content = data.get('content')
    is_completed = data.get('is_completed')
    importance = data.get('importance')

    # Validating content
    if content and not isinstance(content, str):
        raise ValueError("Content must be a string.")

    # Validating is_completed
    if is_completed and not isinstance(is_completed, bool):
        raise ValueError("is_completed must be a boolean.")
    
    # Validating importance
    valid_importance_values = [item.name for item in Importance]
    if 'importance' in data and importance not in valid_importance_values:
        raise ValueError("Invalid importance value.")

@api.route('/', methods=['GET'])
def home():
    return "Welcome to the ToDo API!", 200

@api.route('/todos', methods=['GET'])
def get_all_todos():
    todos = ToDoService.get_all_todos()
    return jsonify([todo.serialize for todo in todos])

@api.route('/todos/completed', methods=['GET'])
def get_completed_todos():
    todos = ToDoService.get_completed_todos()
    return jsonify([todo.serialize for todo in todos])

@api.route('/todos/deleted', methods=['GET'])
def get_deleted_todos():
    todos = ToDoService.get_deleted_todos()
    return jsonify([todo.serialize for todo in todos])

@api.route('/todos', methods=['POST'])
def create_todo():
    try:
        data = request.json
        validate_todo_input(data)
        todo = ToDoService.create_todo(data)
        return jsonify(todo.serialize), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    try:
        data = request.json
        validate_todo_input(data)
        todo = ToDoService.update_todo(id, data)
        return jsonify(todo.serialize)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = ToDoService.delete_todo(id)
    if todo:
        return jsonify({'message': 'Todo marked as deleted.'})
    else:
        return jsonify({'error': 'Failed to delete todo.'}), 400

@api.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = ToDo.query.get(id)
    if not todo:
        return jsonify({"error": "Resource not found"}), 404
    return jsonify(todo.serialize), 200

# Error Handlers
@api.errorhandler(DatabaseError)
def handle_database_error(e):
    db.session.rollback()
    return jsonify({"error": "Database error occurred!"}), 500

@api.errorhandler(404)
def handle_not_found_error(e):
    return jsonify({"error": "Resource not found!"}), 404

@api.errorhandler(400)
def handle_bad_request_error(e):
    return jsonify({"error": "Bad request. Please check the data and try again!"}), 400

@api.errorhandler(500)
def handle_internal_error(e):
    return jsonify({"error": "Internal server error occurred!"}), 500
