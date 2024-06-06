
from flask import Flask,jsonify,request
# from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.models import User
# from app import create_app
from app import db,app
import os
# app=Flask(__name__)
# basedir=os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'db.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# app = create_app()
ma = Marshmallow(app)
# db = SQLAlchemy(app)
# db=SQLAlchemy(app)
#product schema
class UserSchema(ma.Schema):
     class Meta:
        fields=('id','username','email','password_hash')

#init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
# data = ({"id":"1","username":"jhon doe","email":"jhon.doe@gmail.com","password_hash":"boiboi"},
#            {"id":"2","username":"jhon doe","email":"jhon.doe@gmail.com","password_hash":"boiboi"}
#         )
# data1 = {"id":"2","username":"jhon doe","email":"jhon.doe@gmail.com","password_hash":"boiboi"}
# user1=user_schema.load(data)
# user=users_schema.load(data)


@app.route('/apii',methods=['POST'] )
def api_post():
     username=request.json['username']
     email=request.json['email']
     password_hash=request.json['password_hash']

     new_user=User(username,email,password_hash)
     db.session.add(new_user)
     db.session.commit()

     return user_schema.jsonify(new_user)


@app.route('/apii', methods=['GET'] )
def apis_gets():
     all_users=User.query.all()
     result=users_schema.dump(all_users)
     return jsonify(result)


@app.route('/apii/<id>', methods=['GET'] )
def api_get(id):
     all_user=User.query.get(id)
     return user_schema.jsonify(all_user)

@app.route('/mm')
def mm():
    return('hey')



if __name__ == '__main__':
    app.run(debug=True)













# app = create_app()
# if __name__ == '__main__':
#     app.run()
