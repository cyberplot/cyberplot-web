from flask_script import Manager  
from flask_migrate import Migrate, MigrateCommand

from cyberplot.application import create_app  
from cyberplot.models import db, User, Dataset, Space, Attribute, Connector, DatasetVersion, Statistics

app = create_app()
migrate = Migrate(app, db)  
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.shell
def shell_ctx():  
    return dict(app = app,
                db = db,
                User = User,
                Dataset = Dataset,
                Space = Space,
                Attribute = Attribute,
                Connector = Connector,
                DatasetVersion = DatasetVersion,
                Statistics = Statistics)

if __name__ == '__main__':  
    manager.run()