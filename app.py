from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:^&T1F4K3R^&4@localhost:5432/whiskr_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    friends = db.relationship('Friend', backref='user', lazy=True, foreign_keys='Friend.user_id')

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/users')
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'username': user.username}
        output.append(user_data)
    return jsonify({'users': output})

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': f"User '{new_user.username}' created successfully"}), 201



@app.route('/api/friends', methods=['POST'])
def add_friend():
    data = request.get_json()
    user_id = data['user_id']
    friend_id = data['friend_id']

    # Make sure both users exist
    user = User.query.get(user_id)
    friend = User.query.get(friend_id)

    if not user or not friend:
        return jsonify({'error': 'User or friend not found'}), 404

    # Create the friend relationship
    new_friendship = Friend(user_id=user_id, friend_id=friend_id)
    db.session.add(new_friendship)
    db.session.commit()

    return jsonify({'message': 'Friend added successfully'}), 201

@app.route('/api/users/<int:user_id>/friends')
def get_friends(user_id):
    user = User.query.get_or_404(user_id)
    friendships = Friend.query.filter_by(user_id=user_id).all()
    
    friends_list = []
    for friendship in friendships:
        friend_user = User.query.get(friendship.friend_id)
        if friend_user:
            friends_list.append({'id': friend_user.id, 'username': friend_user.username})
            
    return jsonify({'user_id': user.id, 'friends': friends_list})


    if __name__ == '__main__':
        app.run(debug=True)
    #this must remain at the end to register all API endpoints with the app before it runs

    #to activate venv -- .\venv\Script\activate