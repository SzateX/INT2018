class CorsMiddleware(object):
    def process_response(self, req, resp):
        response["Access-Controll-Allow-Origin"] = '*'
        return response
