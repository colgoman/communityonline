from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

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