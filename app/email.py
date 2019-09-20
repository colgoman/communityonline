from flask_mail import Message
from app import mail
from flask import render_template
from app import app
from threading import Thread


def send_email(subject, sender, recipients, text_body, html_body):
    '''
    Email sending wrapper function
    '''
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    '''
    Send email message to user with password reset link.
    '''

    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
                sender=app.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
                html_body=render_template('email/reset_password.html',
                                        user=user, token=token))

def send_async_email(app, msg):
    '''
    Function to run in background thread to send an email.
    '''
    # create application context
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    '''
    Start thread for email sending.
    '''
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()