'''
Define app's API endpoints
'''

from datetime import datetime, timezone
from email.message import EmailMessage
from flask import Blueprint, request, current_app
from build_a_bird.app import utils

API_VERSION = 1

bp = Blueprint('api', __name__, url_prefix=f'/api')

@bp.route('/', methods=['GET'])
def about():
    '''
    Gets info about current API implementation

    Returns a JSON response
    '''

    return {'version': API_VERSION}

@bp.route('/receipt', methods=['POST'])
def receipt():
    '''
    Sends an email receipt based on user's order data

    Returns a JSON response of the form `{"success": bool, "errors": [str]}`
    indicating whether email was sent
    '''

    order_data = None
    try:
        order_data = request.json
    except Exception as e:
        return {'success': False, 'errors': [str(e)]}
    
    # TODO: validate json data according to order inputs (tbd)

    success = True
    errors = []

    email_provider = utils.GmailProvider(current_app.config['APP_EMAIL'], current_app.config['APP_EMAIL_PASSWORD'])

    email = EmailMessage()
    email['Subject'] = f'Build-a-Bird Receipt {datetime.now(tz=timezone.utc)}'
    email['From'] = email_provider.from_addr
    email['To'] = order_data['email_addr']
    email.set_content(str(order_data)) # TODO: write a better message

    errors = email_provider.send(email)
    success = len(errors) == 0

    return {'success': success, 'errors': [f'{addr} = {error}' for addr, error in errors.items()]}

@bp.route('/img', methods=['POST'])
def img():
    '''
    Generates an image of bird based on user's order data

    Returns an image
    '''

    return {'msg': 'work in progress...'}
