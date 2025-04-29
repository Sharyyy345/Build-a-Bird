import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from build_a_bird.app import create_app

# see https://testdriven.io/blog/flask-pytest/

load_dotenv() # load configuration environment variables

class TestAboutEndpoint():
    '''
    Unit tests for Flask app API `about` endpoint
    '''

    def test_get_api_info(self):
        app = create_app()
        app.testing = True

        with app.test_client() as test_client:
            res = test_client.get('/api/')

            assert res.json is not None
            assert res.status_code == 200

            print(res.json)

class TestReceiptEndpoint():
    '''
    Unit tests for Flask app receipt email API endpoint
    '''

    def test_send_mock_receipt_email(self):
        app = create_app()
        app.testing = True

        with app.test_client() as test_client:
            # TODO: base this off actual order inputs
            order_data = {
                'email_addr': app.config['APP_EMAIL'],
                'species': 'conure',
                'color': 'red',
                'personality': 'friendly',
                }
            
            res = test_client.post('/api/receipt', json=order_data)
            
            assert res.json is not None and len(res.json['errors']) == 0
            assert res.status_code == 200
            
            print(res.json)

class TestImgEndpoint():
    '''
    Unit tests for Flask app image generation API endpoint
    '''

    def test_generate_img(self):
        app = create_app()
        app.testing = True

        with app.test_client() as test_client:
            # TODO: base this off actual order inputs
            order_data = {
                'species': 'conure',
                'size': 'small',
                'primary_feather_color': 'red',
                'secondary_feather_color': 'green',
            }

            res = test_client.post('/api/img', json=order_data)

            assert res.json is not None
            assert res.json['success'] == True and len(res.json['errors']) == 0
            assert res.status_code == 200

            # ensure our encoding actually worked and didn't mess up the image
            img = Image.open(BytesIO(base64.b64decode(res.json['img'])))
            img.save('b64_bird.jpg')
