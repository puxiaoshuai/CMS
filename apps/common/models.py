from exts import db
from datetime import datetime


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

#帖子内容
class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"), nullable=False)
    board = db.relationship("BoardModel", backref='posts')
    author = db.relationship('FrontUser', backref='posts')
