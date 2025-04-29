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
