from __future__ import annotations
from O365 import Account
import mimetypes
from typing import Any, Iterable, Optional, Tuple, Union, IO
import logging
import mimetypes
from email.message import EmailMessage
from email import utils
import base64
from ckan.common import _, config

log = logging.getLogger(__name__)
AttachmentWithType = Union[
    Tuple[str, IO[str], str],
    Tuple[str, IO[bytes], str]
]
AttachmentWithoutType = Union[Tuple[str, IO[str]], Tuple[str, IO[bytes]]]
Attachment = Union[AttachmentWithType, AttachmentWithoutType]

class MailerException(Exception):
    pass


from O365 import Account

def _mail_recipient(
        recipient_name: str, recipient_email: str, sender_name: str,
        sender_url: str, subject: Any, body: Any,
        body_html: Optional[Any] = None,
        headers: Optional[dict[str, Any]] = None,
        attachments: Optional[Iterable[Attachment]] = None) -> None:

    if not headers:
        headers = {}

    if not attachments:
        attachments = []

    client_id = config.get('ckanext.moeiemailer.client_id')
    client_secret = config.get('ckanext.moeiemailer.client_secret')
    tenant_id = config.get('ckanext.moeiemailer.tenant_id')
    mail_from = config.get('ckanext.moeiemailer.mail_from')
    credentials = (client_id, client_secret)
    account = Account(credentials, auth_flow_type='credentials', tenant_id=tenant_id)

    if account.authenticate():
        log.info("Authenticated successfully")
        mailbox = account.mailbox(mail_from)
        m = mailbox.new_message()
        m.to.add((recipient_name,recipient_email))
        m.subject = subject
        m.body = body
        if body_html:
            m.body = body_html  # Set HTML body if provided
        
        for attachment in attachments:
            if len(attachment) == 3:
                name, _file, media_type = attachment
            else:
                name, _file = attachment
                media_type = None
            if not media_type:
                media_type, _encoding = mimetypes.guess_type(name)
            if media_type:
                main_type, sub_type = media_type.split('/')
            else:
                main_type = sub_type = None
            m.attachments.add(name)
            attachment = m.attachments[-1]
            attachment.is_inline = True
            attachment.content_id = name
            attachment.content = base64.b64encode(_file.read()).decode('utf-8')

        try:
            m.send()
            log.info("Sent email to {0}".format(recipient_email))
        except Exception as e:
            msg = 'Error sending email: %r' % e
            log.exception(msg)
            raise MailerException(msg)
    else:
        raise MailerException('Authentication failed.')



def mail_recipient(recipient_name: str,
                   recipient_email: str,
                   subject: str,
                   body: str,
                   body_html: Optional[str] = None,
                   headers: Optional[dict[str, Any]] = None,
                   attachments: Optional[Iterable[Attachment]] = None) -> None:

    '''Sends an email to a an email address.

    .. note:: You need to set up the :ref:`email-settings` to able to send
        emails.

    :param recipient_name: the name of the recipient
    :type recipient: string
    :param recipient_email: the email address of the recipient
    :type recipient: string

    :param subject: the email subject
    :type subject: string
    :param body: the email body, in plain text
    :type body: string
    :param body_html: the email body, in html format (optional)
    :type body_html: string
    :headers: extra headers to add to email, in the form
        {'Header name': 'Header value'}
    :type: dict
    :attachments: a list of tuples containing file attachments to add to the
        email. Tuples should contain the file name and a file-like object
        pointing to the file contents::

            [
                ('some_report.csv', file_object),
            ]

        Optionally, you can add a third element to the tuple containing the
        media type. If not provided, it will be guessed using
        the ``mimetypes`` module::

            [
                ('some_report.csv', file_object, 'text/csv'),
            ]
    :type: list
    '''
    site_title = config.get('ckan.site_title')
    site_url = config.get('ckan.site_url')
    return _mail_recipient(
        recipient_name, recipient_email,
        site_title, site_url, subject, body,
        body_html=body_html, headers=headers, attachments=attachments)
    


    


