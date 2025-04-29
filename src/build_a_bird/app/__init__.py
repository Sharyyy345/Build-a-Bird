'''
Initialize `app` module
'''

import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv() # load configuration environment variables

def create_app():
    '''
    Create an instance of the Flask app
    '''
    
    app = Flask(__name__)
    app.static_url_path = os.path.join(app.root_path, 'static') # point to custom static folder

    # store necessary configuration environment variables
    app.config['APP_EMAIL'] = os.getenv('APP_EMAIL', '')
    app.config['APP_EMAIL_PASSWORD'] = os.getenv('APP_EMAIL_PASSWORD', '')
    app.config['DIFFUSERS_MODEL_ID'] = os.getenv('DIFFUSERS_MODEL_ID', 'sd-legacy/stable-diffusion-v1-5') # use legacy stable diffusion v1-5 model by default

    @app.route('/')
    def index():
        res = app.send_static_file('html/index.html') # see https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
        
        return res
    
    @app.route('/about')
    def about():
        res = app.send_static_file('html/about.html')

        return res    
    
    from .routes import api
    app.register_blueprint(api.bp)
        
    return app