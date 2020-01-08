from exts import db
from datetime import datetime


class User(db.Model):
    """
    用户表
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(11), nullable=False)
    user_name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)


class SearchRecord(db.Model):
    """搜索记录表"""
    __tablename = "search_record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    keyword = db.Column(db.String(128), nullable=False)
    search_time = db.Column(db.DateTime, default=datetime.now())
