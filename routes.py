from setup import *
from crud import *

def api_routes(app):

    if app:
        app.add_url_rule('/api/get_info/<string:id>', 'get_info', get_info, methods=['GET'])
        app.add_url_rule('/api/create_doc/<string:collection>', 'create_doc', create_doc, methods=['POST', 'GET'])
