from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    tasks = db.relationship('Task', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default="pending")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def seed_data():
    """Run this manually in Flask shell or app context"""

    user1 = User(username="testuser")
    user1.set_password("password123")

    user2 = User(username="admin")
    user2.set_password("admin123")

    db.session.add_all([user1, user2])
    db.session.commit()

    task1 = Task(
        task_name="Learn Flask JWT",
        description="Understand authentication flow",
        user_id=user1.id
    )

    task2 = Task(
        task_name="Build API",
        description="Create CRUD endpoints",
        user_id=user1.id
    )

    db.session.add_all([task1, task2])
    db.session.commit()

    print("Database seeded successfully!")