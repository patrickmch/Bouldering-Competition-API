from setup import *
class ResponseHandler:
    def create_response(self, result):
        return str(result.raw_result)

        # if result.matched_count < 1:
        #     return
        #     # return "No matching record exists for id %s" % insert[0]["_id"]
        # elif result.modified_count < 1:
        #     return
        #     # return "Failed to update \'%s\' with an id of \'%s\'" % (insert[1]["$set"].keys()[0], insert[0]["_id"])
        # else:
        #     return
        #     # return  "%s record was successfully updated" % str(result.matched_count)



class ErrorResponse(Exception):

    def __init__(self, status_code, message=None, payload=None):
        #TODO put this in a settings file?
        err_messages = {
            400 : 'Some or all of your request was not valid and cannot be processed',
            401 : 'You are not authorized to access the requested resource, either because your credentials are not valid or you did not provide them',
            403 : 'You are not do not have permission to access the requested resource',
            404 : 'The requested resource could not be found',
            500 : 'The server encountered an error'
        }

        Exception.__init__(self)
        if message is None:
            self.message = err_messages[status_code]
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        err_response = dict(self.payload or ())
        err_response['message'] = self.message
        err_response['status_code'] = self.status_code
        return err_response
