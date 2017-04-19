from setup import *
from crud import *
from authenticate_user import *

app = Flask(__name__)
generc_url_args = '<string:id>/<string:collection_name>/'
generic_methods = ['GET', 'POST']
@app.route('/api/create_doc/%s' % generc_url_args, methods= generic_methods)
@require_appkey
def create(collection_name, id):
    return create_doc(collection_name)

@app.route('/api/create_user/', methods= generic_methods)
def create_user():
    return create_doc('participants')

@app.route('/api/find_doc/%s' % generc_url_args, methods= generic_methods)
@require_appkey
def read(collection_name, id):
    return find_doc(collection_name, id)

@app.route('/api/update_doc/%s' % generc_url_args, methods= generic_methods)
@require_appkey
def update(collection_name, id):
    return update_doc(collection_name)

# TODO currently a user can only delete their own profile
@app.route('/api/delete_doc/%s' % generc_url_args, methods= generic_methods)
@require_appkey
def delete(collection_name, id):
    return delete_doc(collection_name, id)
