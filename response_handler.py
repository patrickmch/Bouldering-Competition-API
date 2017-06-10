from setup import *
from settings import err_messages

def create_response(status_code, data=None):
    return flask.jsonify({'status_code' : status_code,'data' : data})

class ErrorResponse(Exception):

    def __init__(self, status_code, message=None, payload=None):
        Exception.__init__(self)
        if message is None:
            self.message = err_messages[status_code]
        else:
            self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        err_response = dict(self.payload or ())
        err_response['message'] = self.message
        err_response['status_code'] = self.status_code
        return flask.jsonify(err_response)
