from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from exts import db
from main import app

manage = Manager(app)
# 使用migrate绑定app
migrate = Migrate(app, db)
# 添加迁移脚本的命令到manger中
manage.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manage.run()
