'''Send messages using MIME and SMTP'''

import os
import smtplib

# Determine which type the attachment is
import mimetypes
from email.message import EmailMessage

class Dev:
    '''SMTP Mail Sender!

    Send a quick message / attachment.

    Example:
        >>> dev = Dev(user=someone@mail.com, password='', host='', port=123)
        >>> dev.open()
        >>> dev.send('Hello!', to=other@mail.com)
        >>> dev.close()
    '''
    def __init__(self, user=None, password=None, host=None, port=None, **kwargs):
        '''
        Args:
            user (str): User name (full email address for login)
            password (str): Password
            host (str): Host server's SMTP address
            port (int): Host server's SMTP Port
        '''
        super(Dev, self).__init__()

        # Server / User information
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # Server connection
        self.server = None

    def open(self):
        '''Open up the connection to the server, and log in.'''
        self.server = smtplib.SMTP(host=self.host, port=self.port)

        # Start the secure connection
        self.server.starttls()
        self.server.login(self.user, self.password)

    def close(self):
        '''Close down the connection to the server'''
        if self.server:
            self.server.quit()
            del self.server

    def send(self, text, *args, to=None, subject=''):
        '''Send text, as well as attachments.

        Args:
            text (str): Message text.
            *args: Attachment files. The MIME type will be guessed, based on
                the file extension.
            to (str): Address to send the message to. Default is user.
            subject (str): Subject of the message. Default is ''.
        '''
        if not to:
            to = self.user

        message = EmailMessage()
        message['From'] = self.user
        message['To'] = to
        message['Subject'] = subject

        # Add message content
        message.set_content(text)

        # Parse attachments
        for attachment in args:
            # Get the MIME Type
            ctype, encoding = mimetypes.guess_type(attachment)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'

            main_type, subtype = ctype.split('/', 1)
            file_name = os.path.basename(attachment)

            with open(attachment, 'rb') as input_file:
                message.add_attachment(input_file.read(), maintype=main_type, subtype=subtype, filename=file_name)

        # Send the message!
        self.server.send_message(message)
