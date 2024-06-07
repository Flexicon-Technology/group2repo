from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
app = Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))

#database
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:guessguess@localhost/firstdb'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'db.stylehub')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False



# Initialize the database connection
db = SQLAlchemy(app)

# Initialize the migration manager
# migrate = Migrate(app, db)

# Initialize the JWT manager
jwt = JWTManager(app)

# Create the database tables before the first request
# @app.before_first_request
# def create_database():
#     db.create_all()

# Import the API resources (blueprint)
from app import resources

# Register the API blueprint with the app
# app.register_blueprint(resources.api_bp, url_prefix='/api')


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('config.Config')

#     db.init_app(app)
#     migrate.init_app(app, db)
#     jwt.init_app(app)

#     from app.resources import api_bp
#     app.register_blueprint(api_bp, url_prefix='/api')

#     return app
