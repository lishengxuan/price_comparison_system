from flask import Flask, render_template
import config

app = Flask(__name__)
# 导入配置文件
app.config.from_object(config)


@app.route("/")
def hello():
    return render_template("index.html")
