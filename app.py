import secrets

from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

from auth import auth
from flask_session import Session
from views import views

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'memory'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(views, url_prefix='/')


CORS(app)

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.spawn = 4
    http_server.serve_forever()
