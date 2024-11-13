from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    nim = db.Column(db.String(80), unique=True, nullable=False)
    nohp = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self) :
        return f"User(name = {self.name}, nim = {self.nim}, nohp = {self.nohp}, email={self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('nim', type=str, required=True, help="NIM cannot be blank")
user_args.add_argument('nohp', type=str, required=True, help="Phone number cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

userField = {
    'id':fields.Integer,
    'name':fields.String,
    'nim':fields.String,
    'nohp':fields.String,
    'email':fields.String,
}

class Users(Resource):
    @marshal_with(userField)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userField)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], nim=args["nim"], nohp=args["nohp"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(userField)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user
    
    @marshal_with(userField)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.name = args["name"]
        user.nim = args["nim"]
        user.nohp = args["nohp"]
        user.email = args["email"]
        db.session.commit()
        return user
    
    @marshal_with(userField)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users
    
class Name(Resource):
    @marshal_with(userField)
    def get(self, name):
        user = UserModel.query.filter_by(name=name).first()
        if not user:
            abort(404, "User not found")
        return user
    
class NIM(Resource):
    @marshal_with(userField)
    def get(self, nim):
        user = UserModel.query.filter_by(nim=nim).first()
        if not user:
            abort(404, "User not found")
        return user
    
class Nohp(Resource):
    @marshal_with(userField)
    def get(self, nohp):
        user = UserModel.query.filter_by(nohp=nohp).first()
        if not user:
            abort(404, "User not found")
        return user
    
class Email(Resource):
    @marshal_with(userField)
    def get(self, email):
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            abort(404, "User not found")
        return user
    
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(Name, '/api/search/nama/<string:name>')
api.add_resource(NIM, '/api/search/nim/<string:nim>')
api.add_resource(Nohp, '/api/search/no_hp/<string:nohp>')
api.add_resource(Email, '/api/search/email/<string:email>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)