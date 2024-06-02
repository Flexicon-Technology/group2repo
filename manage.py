from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # we will replace here with our database uri
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)

  #password hashing!
  password_hash = db.Column(db.String(80), nullable=False)

  @property
  def password(self):
    raise AttributeError('password is not a readable Attribute!')

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password

# for Creating users
@app.route('/users', methods=['POST'])
def create_user():
  data = request.get_json()
  if not data:
    return jsonify({'error': 'No data provided'}), 400

  required_fields = ['username', 'email', 'password']
  if not all(field in data for field in required_fields):
    return jsonify({'error': 'Missing required fields'}), 400

  user = User(**data)
  try:
    db.session.add(user)
    db.session.commit()
  except Exception as e:
    return jsonify({'error': str(e)}), 500

  return jsonify({'message': 'User created successfully'}), 201

if __name__ == '__main__':
  db.create_all()  # This Creates tables if they don't exist
  app.run(debug=True)
