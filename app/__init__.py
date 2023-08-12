from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# Initialize extensions outside of create_app
db = SQLAlchemy()

def page_not_found(e):
    return render_template('404.html'), 404

def internal_server_error(e):
    return render_template('500.html'), 500

def create_app(config_name):
    app = Flask(__name__)

    # Default configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
    
    #Testing Configureation
    if config_name == "testing":
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test_db.sqlite'

    # Bind app instance to extensions
    db.init_app(app)

    # Register error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    #ensure the app instance and db are already create
    from .routes.api import api
    app.register_blueprint(api)

    return app

