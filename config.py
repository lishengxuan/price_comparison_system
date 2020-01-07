import os
DUBUG = True
SECRET_KEY = os.urandom(24)

# 数据库配置
HOSTNAME = os.getenv("HOSTNAME")
POST = os.getenv("POST")
DATABASE = os.getenv("DATABASE")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DB_URI = f'mysql+mysqldb://{USERNAME}:{PASSWORD}@{HOSTNAME}:{POST}/{DATABASE}?charset=utf8'
SQLALCHEMY_DATABASE_URI = DB_URI
