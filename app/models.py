from . import db,app

from werkzeug.security import generate_password_hash, check_password_hash

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

# with app.app_context():
#      db.create_all()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)


