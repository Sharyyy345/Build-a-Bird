'''
Define app's API endpoints
'''

import base64
from datetime import datetime, timezone
from email.message import EmailMessage
from flask import Blueprint, request, current_app
from build_a_bird.app import utils
from io import BytesIO

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
        return {'success': False, 'errors': [str(e)]}, 400
    
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

    Returns a JSON response of the form `{"success": bool, "img": base64(bytes), "errors": [str]}`
    '''

    order_data = None
    try:
        order_data = request.json
    except Exception as e:
        return {'success': False, 'img': '', 'errors': [str(e)]}, 400
    
    # TODO: validate json data according to order inputs (tbd)

    order = utils.BirdOrder(
        species=order_data['species'],
        size=order_data['size'],
        primary_feather_color=order_data['primary_feather_color'],
        secondary_feather_color=order_data['secondary_feather_color'],
        )
    
    img_provider = utils.DiffusersText2ImgProvider(current_app.config['DIFFUSERS_MODEL_ID'], use_gpu=True)

    img = img_provider.gen_img(order)

    # base64 encode in-memory image data for downstream rendering
    # see https://stackoverflow.com/questions/16065694/is-it-possible-to-create-encoded-base64-url-from-image-object
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    img_data = buffer.getvalue()

    return {'success': True, 'img': base64.b64encode(img_data).decode(encoding='utf-8'), 'errors': []}
