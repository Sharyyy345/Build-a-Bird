import smtplib
from email.message import EmailMessage

class GmailProvider():
    '''
    Mechanism for programmatically sending emails via Gmail

    See https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
    '''

    HOST = 'smtp.gmail.com'
    PORT = 465

    def __init__(self, from_addr:str, app_password:str):
        self.from_addr = from_addr
        self.app_password = app_password

    def _connect(self):
        '''
        Establishes a connection to Gmail's SMTP server (with SSL encryption)
        '''

        conn = smtplib.SMTP_SSL(host=self.HOST, port=self.PORT)

        conn.ehlo()

        conn.login(self.from_addr, self.app_password)

        return conn
    
    def send(self, email:EmailMessage):
        '''
        Send `email` via Gmail

        Returns a dictionary, with one entry for each recipient that was refused. 
        Each entry contains a tuple of the SMTP error code and the accompanying error message sent by the server.
        '''

        smtp_conn = self._connect()
        send_errs = smtp_conn.sendmail(self.from_addr, email['To'], email.as_string())
        smtp_conn.quit()
        return send_errs
