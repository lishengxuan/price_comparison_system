from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import config
from models import User, SearchRecord
from exts import db
from public_tools import login_required, run
from settings import HEAD

app = Flask(__name__)
# 导入配置文件
app.config.from_object(config)
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search_detail")
@login_required
def search_detail():
    return "搜索详情"


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    登录
    """
    if request.method == "GET":
        return render_template("login.html")
    else:
        phone = request.form.get("phone")
        password = request.form.get("password")
        user = db.session.query(User).filter(User.phone == phone).first()
        if not user:
            return "手机号未被注册请注册"
        # 判断密码是否正确
        user_password = user.password
        if check_password_hash(user_password, password):
            session["user_id"] = user.id
            return redirect(url_for("index"))
        else:
            return "密码输入有误"


@app.route("/regist", methods=["GET", "POST"])
def regist():
    """
    注册
    """
    if request.method == "GET":
        return render_template("regist.html")
    else:
        user_name = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        phone = request.form.get("telephone")
        user_obj = db.session.query(User).filter(or_(User.phone == phone, User.user_name == user_name)).first()
        if user_obj:
            return "该手机号或者用户名已经被使用！"
        if not user_name or not password1 or not password2 or not phone:
            return "缺少参数请检查！"
        if password1 != password2:
            return "两次密码输入不相同！"
        # 保存数据
        user = User()
        user.password = generate_password_hash(password1)
        user.user_name = user_name
        user.phone = phone
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """注销"""
    session.clear()
    return redirect(url_for("login"))


# 钩子函数判断用户是否登录
@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = db.session.query(User).filter(User.id == user_id).first()
        if user:
            return {"user": user}
    return {}


@app.route("/search_goods")
@login_required
def search_goods():
    """
    搜索商品保存到数据库中
    """
    keyword = request.args.get("keyword")
    keyword = str(keyword)
    if keyword:
        # 判断用户是否登录
        if session.get("user_id"):
            user = db.session.query(User).filter(User.id == session.get("user_id")).first()
            if user:
                # 创建搜索记录
                search_record = SearchRecord()
                search_record.user_id = user.id
                search_record.keyword = keyword
                db.session.add(search_record)
                db.session.commit()
                db.session.flush()
                search_record_id = str(search_record.id)
                run(keyword, HEAD, search_record_id)
                return "爬虫完成，稍后到搜索记录中查看！"
    else:
        return "请输入关键字"

