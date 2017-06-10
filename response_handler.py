from setup import *

def create_response(status_code, data=None):
    return flask.jsonify({'status_code' : status_code,'data' : data})

class ErrorResponse(Exception):

    def __init__(self, status_code, message=None, payload=None):
        #TODO put this in a settings file?
        err_messages = {
            400 : 'Some or all of your request was not valid and cannot be processed',
            401 : 'You are not authorized to access the requested resource, either because your credentials are not valid or you did not provide them',
            403 : 'You do not have permission to access the requested resource',
            404 : 'The requested resource could not be found',
            500 : 'The server encountered an error'
        }

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
