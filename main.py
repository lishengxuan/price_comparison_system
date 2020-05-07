import json
from datetime import datetime

import pymongo
from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import or_, text
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
    if request.method == "GET":
        # 查询当前用户的搜索记录
        user_id = session.get("user_id")
        search_list = db.session.query(SearchRecord).filter(SearchRecord.user_id == user_id).order_by(
            text("-search_time")).all()
        return render_template("search_list.html", search_list=search_list)


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
                search_record.search_time = datetime.now()
                db.session.add(search_record)
                db.session.commit()
                db.session.flush()
                search_record_id = str(search_record.id)
                run(keyword, HEAD, search_record_id)
                return redirect(url_for("search_detail"))
    else:
        return "请输入关键字"


@app.route("/search_goods_detail")
@login_required
def search_goods_detail():
    """查询送所记录详情"""
    search_id = request.args.get("id")
    # 创建mongodb对象
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['runoobdb']
    mycol = mydb[str(search_id)]
    info_list = []
    for x in mycol.find().sort("price", -1):
        info_list.append(x)
    return render_template("info_list.html", info_list=info_list, search_id=search_id)


@app.route("/sector_chart")
@login_required
def get_sector_chart():
    """获取扇形图"""
    search_id = request.args.get("id")
    # 创建mongodb对象
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['runoobdb']
    mycol = mydb[str(search_id)]
    info_list = []
    # 0-2000个数
    first_count = 0
    # 2000-4000个数
    second_count = 0
    # 4000-6000个数
    third_count = 0
    # 6000-8000个数
    fourth_count = 0
    # 8000以上个数
    fifth_list = 0
    for x in mycol.find().sort("price", -1):
        info_list.append(x)
    # 商品总个数
    goods_count = len(info_list)
    # 数据分析（将价位分为0-2000，2000-4000。。。。8000-以上,以及8000以上的5个等级）
    for i in info_list:
        if i.get("price"):
            if 0 < i.get("price") <= 2000:
                first_count += 1
            elif 2000 < i.get("price") <= 4000:
                second_count += 1
            elif 4000 < i.get("price") <= 6000:
                third_count += 1
            elif 6000 < i.get("price") <= 8000:
                fourth_count += 1
            else:
                fifth_list += 1
            # 扇形图返回的数据
    sector_chart_list = [['0-2000', float(first_count / goods_count)],
                         ['2000-4000', float(second_count / goods_count)],
                         ['4000-6000', float(third_count / goods_count)],
                         ['6000-8000', float(fourth_count / goods_count)],
                         ['8000以上', float(fifth_list / goods_count)]]
    return render_template("sector_chart.html", result_json=json.dumps(sector_chart_list))
