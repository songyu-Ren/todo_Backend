from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# Initialize the Flask-SQLAlchemy extension instance
# Doing this outside create_app allows multiple app instances
# to share the same database connection
db = SQLAlchemy()

# Error handler for 404 - Page Not Found
def page_not_found(e):
    return render_template('404.html'), 404

# Error handler for 500 - Internal Server Error
def internal_server_error(e):
    return render_template('500.html'), 500

def create_app(config_name):

    # Create a Flask app instance
    app = Flask(__name__)

    # Default configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'

    # If the app is being run in testing mode, 
    # update configurations accordingly
    if config_name == "testing":
        app.config['TESTING'] = True
        # Use a separate SQLite database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test_db.sqlite'

    # Attach the database instance to the Flask app instance
    db.init_app(app)

    # Register error handlers to app
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    # Importing and registering the API blueprint
    #ensure the app instance and db are already create
    from .routes.api import api
    app.register_blueprint(api)

    return app

