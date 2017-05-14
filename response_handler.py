from setup import g
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

    def error_response(self, error):
        return str(error)
