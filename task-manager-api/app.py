from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

from config import Config
from models import db, bcrypt, User, Task

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# ---------------- AUTH ----------------

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data.get('username') or not data.get('password'):
        return {"error": "Missing fields"}, 400

    if User.query.filter_by(username=data['username']).first():
        return {"error": "User already exists"}, 400

    user = User(username=data['username'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return {"message": "User created"}, 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get('username')).first()

    if not user or not user.check_password(data.get('password')):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity=str(user.id))

    return {"access_token": token}, 200


@app.route('/me')
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user.id,
        "username": user.username
    }, 200


# ---------------- TASKS ----------------

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get('task_name'):
        return {"error": "Task name required"}, 400

    task = Task(
        task_name=data['task_name'],
        description=data.get('description'),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return {"message": "Task created"}, 201


@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    tasks = Task.query.filter_by(user_id=user_id).all()

    return {
        "tasks": [
            {
                "id": t.id,
                "task_name": t.task_name,
                "description": t.description,
                "status": t.status
            } for t in tasks
        ]
    }, 200


@app.route('/tasks/<int:id>/complete', methods=['PATCH'])
@jwt_required()
def complete_task(id):
    user_id = int(get_jwt_identity())
    task = Task.query.get(id)

    if not task:
        return {"error": "Not found"}, 404

    if task.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    task.status = "done"
    db.session.commit()

    return {"message": "Task completed"}, 200


@app.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    user_id = int(get_jwt_identity())
    task = Task.query.get(id)

    if not task:
        return {"error": "Not found"}, 404

    if task.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    db.session.delete(task)
    db.session.commit()

    return {"message": "Task deleted"}, 200


# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)