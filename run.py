from app import create_app, db
from app.models import ToDo

app = create_app('development') 

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
