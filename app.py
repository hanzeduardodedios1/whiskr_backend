from flask import Flask
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:^&T1F4K3R^&4@localhost:5432/whiskr_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))



@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()

@app.route('/api/users')
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'username': user.username}
        output.append(user_data)
    return jsonify({'users': output})


@app.route('/api/users', methods=['POST']) #tells Flask to handle a POST request to /api/users endpoint
def add_user():
    data = request.get_json() # this gets JSON data sent from the app
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit() #SQLAlchemy commands to add and save new users to database
    return jsonify({'message': f"User '{new_user.username}' created successfully"}), 201