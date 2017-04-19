from setup import *
from routes import api_routes
from crud import *

app = Flask(__name__)


@app.route('/api/create_doc/<string:id>/<string:collection_name>', methods=['GET', 'POST'])
@require_appkey
def create(collection_name, id):
    return create_doc(collection_name)

@app.route('/api/create_user/', methods=['GET', 'POST'])
def create_user():
    return create_doc('participants')

@app.route('/api/find_doc/<string:collection_name>/<string:id>', methods=['GET', 'POST'])
@require_appkey
def read(collection_name, id):
    return find_doc(collection_name, id)

@app.route('/api/update_doc/<string:collection_name>', methods=['GET', 'POST'])
@require_appkey
def update(collection_name, id):
    return update_doc(collection_name)

@app.route('/api/delete_doc/<string:id>/<string:collection_name>', methods=['GET', 'POST'])
@require_appkey
def delete(collection_name, id):
    return delete_doc(collection_name)
