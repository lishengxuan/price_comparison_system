import os

DUBUG = True
SECRET_KEY = os.urandom(24)
# 数据库配置
HOSTNAME = os.getenv("HOSTNAME")
PORT = os.getenv("PORT", 3306)
DATABASE = os.getenv("DATABASE")
USERNAME = os.getenv("USERNAME", "root")
PASSWORD = os.getenv("PASSWORD")
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


