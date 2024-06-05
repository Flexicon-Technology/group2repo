# Import the necessary modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Create a new Flask app
app = Flask(__name__)

# Configure the app to use a Postgres database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shayo2006@localhost:/stylehub'

# Initialize the database connection
db = SQLAlchemy(app)

# Initialize the migration manager
migrate = Migrate(app, db)

# Initialize the JWT manager
jwt = JWTManager(app)

# Create the database tables before the first request
@app.before_first_request
def create_database():
    db.create_all()

# Import the API resources (blueprint)
from app import resources

# Register the API blueprint with the app
app.register_blueprint(resources.api_bp, url_prefix='/api')

# Run the app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)