'''Send messages using MIME and SMTP'''

import os
import smtplib

# Determine which type the attachment is
import mimetypes
import email.mime.multipart as multipart

# Message attachments
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage

# Encoder for unknown attachment type
from email import encoders

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
        
        message = multipart.MIMEMultipart()
        message['From'] = self.user
        message['To'] = to
        message['Subject'] = subject
        
        # Parse attachments
        for attachment in args:
            message.attach(self._get_attachment(attachment))
        
        # Attach the text
        message.attach(MIMEText(text, 'plain'))
        
        # Send the message!
        self.server.send_message(message)
        
    def _get_attachment(self, file_path):
        '''Form the attachment.
        
        Args:
            file_path (str): Path to the attachment.
        
        Returns:
            The Attachment.
        '''
        # Get the MIME Type
        ctype, encoding = mimetypes.guess_type(file_path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        
        main_type, subtype = ctype.split('/', 1)
        
        # Form the attachment
        with open(file_path, 'r') as input_file:
            if main_type == 'text':
                attachment = MIMEText(input_file.read(), _subtype=subtype)
            elif main_type == 'image':
                attachment = MIMEImage(input_file.read(), _subtype=subtype)
            elif main_type == 'audio':
                attachment = MIMEAudio(input_file.read(), _subtype=subtype)
            else:
                attachment = MIMEBase(main_type, subtype)
                attachment.set_payload(input_file.read())
                encoders.encode_base64(attachment)
        
        # Get the file name
        file_name = os.path.basename(file_path)
        
        # Set the Header
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        
        return attachment
