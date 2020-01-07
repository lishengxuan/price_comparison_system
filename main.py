from flask import Flask, render_template, request
import config

app = Flask(__name__)
# 导入配置文件
app.config.from_object(config)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    登录
    """
    if request.method == "GET":
        return render_template("login.html")
    else:
        return "登录"


@app.route("/regist", methods=["GET", "POST"])
def regist():
    """
    注册
    """
    if request.method == "GET":
        return render_template("regist.html")
    else:
        return "注册"
