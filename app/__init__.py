# # crud_app/app/__init__.py
# from flask import Flask

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('config.Config')

#     with app.app_context():
#         from . import routes

#         return app




from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    try:
        app.config.from_object(Config)
        db.init_app(app)
        # print(db)
        
        from app.routes import main
        app.register_blueprint(main)

        try:
            # print(app.app_context())
            with app.app_context():
                db.create_all()
                # session = db.session
                return app
        except Exception as e:
            print(e)
        
    except Exception as e:
        print(e,"failed config")
