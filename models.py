from exts import db


class User(db.Model):
    """
    用户表
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(11), nullable=False)
    user_name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
