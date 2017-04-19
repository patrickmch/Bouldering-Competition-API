from setup import *
from routes import api_routes
from crud import *

app = Flask(__name__)

api_routes(app)

@app.route('/')
def index():
    return 'Index'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/api/create_doc/<string:id>/<string:collection_name>', methods=['GET', 'POST'])
@require_appkey
def create_user(collection_name):
    return create_doc(collection_name)
