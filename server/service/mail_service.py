import os

from flask_mail import Mail, Message
from flask import render_template


class MailService():

    def __init__(self):
        self.ADMIN_SENDER = os.environ.get('ADMIN_SENDER')
        self.MAIL_SERVER = os.environ.get('MAIL_SERVER')
        self.MAIL_PORT = 465
        self.MAIL_USE_TLS = False
        self.MAIL_USE_SSL = True
        self.MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        self.MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        self.msg = {}
        self.content = '',
        self.link = '',
        self.recipient = []

    def reset_password_mail(self, email):
        email['config'].config['MAIL_SERVER'] = self.MAIL_SERVER
        email['config'].config['MAIL_PORT'] = self.MAIL_PORT
        email['config'].config['MAIL_USE_TLS'] = self.MAIL_USE_TLS
        email['config'].config['MAIL_USE_SSL'] = self.MAIL_USE_SSL
        email['config'].config['MAIL_USERNAME'] = self.MAIL_USERNAME
        email['config'].config['MAIL_PASSWORD'] = self.MAIL_PASSWORD
        mail = Mail(email['config'])
        self.link = email['link']
        self.recipient = email['recipient']
        self.content = self.__contribution_template()
        msg = Message(
            'Reset Password Link',
            sender=self.ADMIN_SENDER,
            recipients=self.recipient,
            **self.content
        )
        mail.send(msg)

    def __contribution_template(self):
        self.msg['body'] = 'Reset Password Link'
        self.msg['html'] = render_template(
            "email_template.html",
            link=self.link
        )
        return self.msg
