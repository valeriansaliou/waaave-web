import json

from django.http import HttpResponse



class APIHelper(object):
    """
    An helper on API operations
    """

    @staticmethod
    def response(status='error', message='', contents={}, http_code=200):
        """
        Return the API response object
        """
        return HttpResponse(
            json.dumps({
                'status': status,
                'message': message,
                'contents': contents,
            }),

            content_type='application/json',
            status=http_code,
        )
