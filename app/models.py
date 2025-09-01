from app import db

class Task(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable=False)
    status = db.Column(db.String(20),default='Pending')

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),unique=True,nullable=False)
    password = db.Column(db.String(150),nullable=False)
    email = db.Column(db.String(200),nullable=False,unique=True)