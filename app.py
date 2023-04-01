from pathlib import Path
from flask import Flask, jsonify, session, url_for, request, render_template
from flask_cors import CORS, cross_origin
from flask_restx  import Api
from controllers.CartController import CartController
from controllers.InventoryController import InventoryController
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
import http.client

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)
api = Api(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
api.add_resource(CartController, '/cart')
api.add_resource(InventoryController, '/inventory')
api.secret_key = os.getenv("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

app.secret_key = os.getenv("APP_SECRET_KEY")

if __name__ == "__main__":
    # start up api
    app.run(port=os.getenv('HOST_PORT'), debug=True)