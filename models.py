from app import db
import app

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    completed = db.Column(db.Boolean, default=False)

