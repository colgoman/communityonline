from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
<<<<<<< HEAD
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from config import Config
=======
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
>>>>>>> parent of aaa9c08... Restructured application by seperate subsytems

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_message = _l('Please log in to access this page.')
<<<<<<< HEAD
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # add new elasticsearch app instance, set isntance to be None when a URL is not present for the service
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
=======
login.login_view = 'login'
mail = Mail(app)
Bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)
>>>>>>> parent of aaa9c08... Restructured application by seperate subsytems


from app import routes, models, errors

# only enable email logger when application not in debug mode
if not app.debug:
    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr = 'no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'], subject = 'Microblog Failure',
        credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
        

<<<<<<< HEAD
    

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
=======
>>>>>>> parent of aaa9c08... Restructured application by seperate subsytems

    # file based logger
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # limit size of log file and keep last 10 log files for backup
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    # custom formatting for log messages - timestamp, logging level, message, sourcefile and log number
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # lower logging level to INFO category
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog statup')


    
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


