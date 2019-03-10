from apps.extend import celery
from flask_mail import Message
from apps import config
from flask import render_template
from apps.extend import mail

@celery.task()
def send_register_active_email(to_email, username, uid):
    """发送邮件"""
    subject = '欢迎你'
    html = render_template('mail.html', username=username, uid=uid, token='wowowow')
    msg = Message(subject=subject, html=html, sender=config.Config.MAIL_USERNAME, recipients=[to_email])
    mail.send(msg)
