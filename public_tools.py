import time
from functools import wraps
from lxml import etree
import pymongo
import requests
from flask import session, redirect, url_for


def login_required(func):
    """登录限制装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_id"):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return wrapper


def str_to_int_type(str_data):
    """将字符串类型转换为int类型"""
    if str_data:
        int_data = float(str_data)
    else:
        int_data = None
    return int_data


def save_data_in_mongodb(set_name, json_data):
    """
    保存数据到mongodb中
    """
    # 创建mongodb对象
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['runoobdb']
    mycol = mydb[set_name]
    mycol.insert_many(json_data)


def craw_jd_goods(url, head):
    """爬取数据"""
    r = requests.get(url, headers=head)
    # 指定编码方式，不然会出现乱码
    r.encoding = 'utf-8'
    html = etree.HTML(r.text)
    # 定位到每一个商品标签li
    datas = html.xpath('//li[contains(@class,"gl-item")]')
    good_list = []
    for data in datas:
        good_dict = {}
        # 商品价格
        price = data.xpath('div/div[@class="p-price"]/strong/i/text()')
        # 商品选购指数
        purchase_index = data.xpath('div/div[@class="p-commit"]/span[@class="buy-score"]/em/text()')
        # 商品名称
        name = data.xpath('div/div[@class="p-name p-name-type-2"]/a/em/text()')
        # 商品购买链接
        url = data.xpath('div/div[@class="p-commit"]/strong/a/attribute::href')
        # 商品图片
        img = data.xpath('div/div[@class="p-img"]/a/img/attribute::source-data-lazy-img')
        # 这个if判断用来处理那些价格可以动态切换的商品，小米MIX2，他们的价格位置在属性中放了一个最低价
        if len(price) == 0:
            price = data.xpath('div/div[@class="p-price"]/strong/@data-price')
        # 将price转换为int类型
        price = str_to_int_type(price[0] if price else None)
        # 将purchase_index转化为int类型
        purchase_index = str_to_int_type(purchase_index[0] if purchase_index else None)
        good_dict.update({"price": price,
                          "purchase_index": purchase_index,
                          "name": name[0] if name else None,
                          "url": url[0] if url else None,
                          "img": img[0] if img else None})
        good_list.append(good_dict)
    return good_list


def run(keyword, head, set_name):
    """主函数"""
    good_list = []
    # 每种商品的total为100页，所以要构造100*2个url
    for i in range(1, 2):
        # 休眠一秒，防止网络延迟，xpath获取不到页面数据
        time.sleep(1)
        print(i)
        # 每页的URL分为前30条数据和后30条数据
        first_url = f'https://search.jd.com/Search?keyword={keyword}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=' + str(
            2 * i - 1)
        now_time = time.time()
        now_time_format = '%.5f' % now_time
        last_url = f'https://search.jd.com/s_new.php?keyword={keyword}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=' + str(
            2 * i) + '&s=' + str(48 * i - 20) + '&scrolling=y&log_id=' + str(now_time_format)
        first_good_list = craw_jd_goods(first_url, head)
        last_good_dict = craw_jd_goods(last_url, head)
        good_list = first_good_list + last_good_dict
    # 将数据保存到mongodb中
    save_data_in_mongodb(set_name, good_list)
