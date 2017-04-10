from flask import jsonify
from flask import render_template
from flask import flash
from flask import current_app
from flask import abort

from crud import *

def api_routes(app):

    if app:
        app.add_url_rule('/api/get_info/<string:id>', 'get_info', get_info, methods=['GET'])
        app.add_url_rule('/api/create_participant', 'create_participant', create_participant, methods=['POST', 'GET'])
