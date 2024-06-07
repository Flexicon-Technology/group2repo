
from flask import Flask,jsonify,request
from flask_marshmallow import Marshmallow
from app.models import User
# from app import create_app
from app import db,app
import os
ma = Marshmallow(app)
#product schema
class UserSchema(ma.Schema):
     class Meta:
        fields=('id','username','email','password_hash')

#init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/apii',methods=['POST'] )
def api_post():
     username=request.json['username']
     email=request.json['email']
     password_hash=request.json['password_hash']

     new_user=User(username,email,password_hash)
     db.session.add(new_user)
     db.session.commit()

     return user_schema.jsonify(new_user)


@app.route('/userapi', methods=['GET'] )
def apis_gets():
     all_users=User.query.all()
     result=users_schema.dump(all_users)
     return jsonify(result)


@app.route('/userapi/<id>', methods=['GET'] )
def api_get(id):
     all_user=User.query.get(id)
     return user_schema.jsonify(all_user)

@app.route('/userapi/<id>',methods=['PUT'])
def update_product(id):
     user=User.query.get(id)
     username=request.json['username']
     email=request.json['email']
     password_hash=request.json['password_hash']

     user.username=username
     user.email=email
     user.password_hash=password_hash

     db.session.commit()

     return user_schema.jsonify(user)

#delete user
@app.route('/userapi/<id>',methods=['DELETE'])
def delete_product(id):
     user=User.query.get(id)
     db.session.delete(user)
     db.session.commit()
     return user_schema.jsonify(user)
