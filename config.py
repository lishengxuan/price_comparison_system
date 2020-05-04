import os

DUBUG = True
SECRET_KEY = os.urandom(24)
# 数据库配置
# HOSTNAME = os.getenv("HOSTNAME", "127.0.0.1")
# PORT = os.getenv("PORT", 3306)
# DATABASE = os.getenv("DATABASE", "price_sys_db")
# USERNAME = os.getenv("USERNAME", "root")
# PASSWORD = os.getenv("PASSWORD", 'root')
HOSTNAME = "127.0.0.1"
PORT = 3306
DATABASE = "price_sys_db"
USERNAME = "root"
PASSWORD = "root"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
