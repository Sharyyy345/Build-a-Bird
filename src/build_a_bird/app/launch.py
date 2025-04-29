'''
Launch an instance of the Flask app
'''

from build_a_bird.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
    