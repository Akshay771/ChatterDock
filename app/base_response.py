from flask import jsonify, make_response


class BaseResponse(object):

    def __init__(self, code=200, result={}, message='Success', error='', error_detail={}, user_name=None):
        self.code = code
        self.result = result
        self.message = message
        self.error = error
        self.error_detail = error_detail
        self.total_data = None
        self.total_page = None
        self.page = None
        self.limit = None
        self.data_message = None
        self.user_name = user_name

    def json(self):
        # standard response
        pagination = {"total_data": self.total_data, "total_page": self.total_page, "page": self.page,
                      "limit": self.limit} if self.total_data is not None else {}
        self.result = self.result if self.result else []
        response = {
            "user_name": self.user_name,
            "meta": {
                "status_code": self.code,
                "error": self.error,
                "message": self.message,
                "error_detail": self.error_detail
            },
            "data": self.result,
            "message": self.data_message,
            "pagination": pagination
        }

        return make_response(jsonify(response), self.code)
