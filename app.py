from setup import *
from crud import *
from authenticate_user import *

app = Flask(__name__)

# create variable/function with generic info to keep the code DRY
# all urls take function to call, and (with the exception of create_user) take an id (used as api_key) and the
# collection_name of collection to be modified
generic_methods = ['GET', 'POST']
def url_string(func_to_call):
    return '/api/%s/<string:id>/<string:collection_name>/' % func_to_call

#url rules
@app.route(url_string('create_doc'), methods= generic_methods)
@require_appkey
def create(collection_name, id):
    return create_doc(collection_name)

@app.route('/api/create_user/', methods= generic_methods)
def create_user():
    return create_doc('participants')

@app.route(url_string('find_doc'), methods= generic_methods)
@require_appkey
def read(collection_name, id):
    return find_doc(collection_name, id)

@app.route(url_string('update_doc'), methods= generic_methods)
@require_appkey
def update(collection_name, id):
    return update_doc(collection_name)

@app.route(url_string('delete_doc'), methods= generic_methods)
@require_appkey
def delete(collection_name, id):
    return delete_doc(collection_name, id)
