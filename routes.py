from setup import *
from crud import *

def api_routes(app):

    if app:
        app.add_url_rule('/api/find_doc/<string:collection_name>/<string:id>', 'find_doc', find_doc, methods=['GET', 'POST'])
        # app.add_url_rule('/api/create_doc/<string:collection_name>', 'create_doc', create_doc, methods=['POST', 'GET'])
        app.add_url_rule('/api/update_doc/<string:collection_name>', 'update_doc', update_doc, methods=['GET', 'POST'])
        app.add_url_rule('/api/delete_doc/<string:collection_name>/<string:id>', 'delete_doc', delete_doc, methods=['GET', 'POST'])
