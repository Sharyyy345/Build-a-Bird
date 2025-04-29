'''
Define app's API endpoints
'''

from flask import Blueprint

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

    Returns a JSON response of the form `{success: true/false}`
    indicating whether email was sent
    '''

    return {'success': True}

@bp.route('/img', methods=['POST'])
def img():
    '''
    Generates an image of bird based on user's order data

    Returns an image
    '''

    return {'msg': 'work in progress...'}
