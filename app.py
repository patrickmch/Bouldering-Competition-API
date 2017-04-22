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
@filter_request
def create(**kwargs):
    new_doc = Crud(**kwargs)
    return new_doc.create_doc()

@app.route('/api/create_user/', methods= generic_methods)
@filter_request
def create_user(request):
    # this is a bit of a hack: pass some irrelevant info to crud
    user = Crud(collection_name = 'participants',_id = 0, user = request, request = request)
    return user.create_doc()

@app.route(url_string('find_doc'), methods= generic_methods)
@filter_request
def read(**kwargs):
    new_search = Crud(**kwargs)
    return new_search.find_doc()

@app.route(url_string('update_doc'), methods= generic_methods)
@filter_request
def update(**kwargs):
    update = Crud(**kwargs)
    return update.update_doc()

@app.route(url_string('delete_doc'), methods= generic_methods)
@filter_request
def delete(**kwargs):
    delete = Crud(**kwargs)
    return delete.delete_doc()
