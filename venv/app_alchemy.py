from flask import Flask
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "clave_secreta_segura"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///datos.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
