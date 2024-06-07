from flask_restful import Resource, Api
from flask import Flask, request, redirect, url_for, flash, render_template
from flask_login import LoginManager, login_user, UserMixin
import psycopg2, psycopg2.extras

app = Flask(__name__)
api = Api(app)

# Database connection
DB_HOST = 'localhost'
DB_NAME= 'the_database_name'
DB_USER = 'the_database_username'
DB_PASSWORD = 'the_database_ password'

# Initializing login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Database connection function
def connection():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

# Function to find user
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        
    def find_user(cls, username):
        conn = connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        if user_data:
            return cls(user_data['id'], user_data['username'], user_data['password'])
        return None
    
    def check_password(self, password):
        return (self.password, password)
    
# Function for user loader
@login_manager.user_loader
def load_user(cls, id):
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    if user_data:
        return cls(user_data['id'], user_data['username'], user_data['password'])
    return None
    

# Function to create login route    
@app.route('/<int:id>/login', methods=['GET', 'POST'])
def login(id):       
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.find_user(username)
            
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")
                
        return render_template('login.html')
                