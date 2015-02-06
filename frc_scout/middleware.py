class ContentLengthMiddleware(object):
    def process_response(self, request, response):
        response['Content-Length'] = str(len(response.content))
        return response