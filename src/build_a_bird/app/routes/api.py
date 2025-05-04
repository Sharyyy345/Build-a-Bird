'''
Define app's API endpoints
'''

import base64
from datetime import datetime, timezone
from email.message import EmailMessage
from flask import Blueprint, request, current_app
from build_a_bird.app import utils, entities
from io import BytesIO

API_VERSION = 1

bp = Blueprint('api', __name__, url_prefix=f'/api')

@bp.route('/', methods=['GET'])
def about():
    '''
    Gets info about current API implementation

    Returns a JSON response formatted based on `ApiResponse` object
    '''

    res = utils.ApiResponse()

    res.data = {'version': API_VERSION}

    return res.to_json(), res.status_code

@bp.route('/receipt', methods=['POST'])
def receipt():
    '''
    Sends an email receipt based on user's order data

    Returns a JSON response formatted based on `ApiResponse` object
    '''

    res = utils.ApiResponse()

    order_data = None
    try:
        order_data = request.json
    except Exception as e:
        res.success = False
        res.errors = [e]
        res.status_code = 400

        return res.to_json(), res.status_code
        
    order = entities.BirdOrder()
    loaded = order.from_json(order_data) # validate input json data

    if not loaded[0]:
        # order json data is invalid in some way
        res.success = False
        res.errors = [loaded[1]]
        res.status_code = 400

        return res.to_json(), res.status_code

    email_provider = utils.GmailProvider(current_app.config['APP_EMAIL'], current_app.config['APP_EMAIL_PASSWORD'])

    # construct email
    email = EmailMessage()
    email['Subject'] = f'Build-a-Bird Receipt {datetime.now(tz=timezone.utc)}'
    email['From'] = email_provider.from_addr
    email['To'] = order.user_email
    content = f'Hi {order.user_name},\n\nThanks for buying a feathered friend from Build-a-Bird! Your receipt is below.\n\n{str(order)}'
    email.set_content(content)

    try:
        errors = email_provider.send(email)
        if len(errors) != 0:
            res.success = False
            res.errors = [f'Send failed for {addr} with error {error}' for addr, error in errors.items()]
            res.status_code = 400
    except Exception as e:
        res.success = False
        res.errors = [str(e)]
        res.status_code = 400
        
    res.data = content

    return res.to_json(), res.status_code

@bp.route('/img', methods=['POST'])
def img():
    '''
    Generates an image of bird based on user's order data

    Returns a JSON response formatted based on `ApiResponse` object
    '''

    res = utils.ApiResponse()

    order_data = None
    try:
        order_data = request.json
    except Exception as e:
        res.success = False
        res.errors = [str(e)]
        res.status_code = 400

        return res.to_json(), res.status_code
    
    order = entities.BirdOrder()
    loaded = order.from_json(order_data) # validate input json data

    if not loaded[0]:
        # order json data is invalid in some way
        res.success = False
        res.errors = [loaded[1]]
        res.status_code = 400

        return res.to_json(), res.status_code
    
    img_provider = utils.DiffusersText2ImgProvider(
        current_app.config['DIFFUSERS_MODEL_ID'], 
        img_size=current_app.config['IMG_SIZE'],
        device=current_app.config['MODEL_DEVICE'],
    )

    img = img_provider.gen_img(order)

    # base64 encode in-memory image data for downstream rendering
    # see https://stackoverflow.com/questions/16065694/is-it-possible-to-create-encoded-base64-url-from-image-object
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    img_data = buffer.getvalue()

    res.data = base64.b64encode(img_data).decode(encoding='utf-8')

    return res.to_json(), res.status_code
