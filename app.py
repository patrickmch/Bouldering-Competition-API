from setup import *
from routes import api_routes

app = Flask(__name__)

api_routes(app)

@app.route('/')
def index():
    return 'Index'

@app.route('/hello')
def hello():
    return 'Hello, World'
