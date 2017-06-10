# imports that are used in most files
from flask import abort, g
import flask
import pymongo
import flask_login
import passlib.context
import bson
from response_handler import create_response, ErrorResponse
# database and colllection setup
login_manager = flask_login.LoginManager()
client = pymongo.MongoClient()
db = client.test
# passlib; documentation at https://passlib.readthedocs.io/en/stable/narr/quickstart.html
pwd_encrypt = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
