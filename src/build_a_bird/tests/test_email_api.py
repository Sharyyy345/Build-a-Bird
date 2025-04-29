import os
from dotenv import load_dotenv
from email.message import EmailMessage
from build_a_bird.app import utils

load_dotenv() # load configuration environment variables

class TestGmailProvider():
    '''
    Unit tests for `GmailProvider` email provider
    '''

    def test_send_email_self(self):
        '''
        Test sending an email to yourself via Gmail
        '''

        from_addr = os.getenv('APP_EMAIL')
        app_email_password = os.getenv('APP_EMAIL_PASSWORD')

        email_provider = utils.GmailProvider(from_addr, app_email_password)
        
        # see https://stackoverflow.com/questions/6270782/how-to-send-an-email-with-python
        email = EmailMessage()
        email['Subject'] = 'Testing 123'
        email['From'] = from_addr
        email['To'] = from_addr # send to yourself just for testing
        email.set_content('This is a test email. Hopefully you received it...')

        send_errs = email_provider.send(email)

        assert len(send_errs) == 0
