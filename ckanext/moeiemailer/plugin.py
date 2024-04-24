from ckanext.moeiemailer.emailer import mail_recipient

import ckan
import ckan.plugins as p

ckan.lib.mailer.mail_recipient = mail_recipient    # noqa

class MailerMoei(p.SingletonPlugin):
    ckan.lib.mailer.mail_recipient = mail_recipient 
