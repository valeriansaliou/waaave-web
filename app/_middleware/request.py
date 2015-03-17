class XForwardedForMiddleware():
    """
    Maps the proxy-generated 'HTTP_X_FORWARDED_FOR' to 'REMOTE_ADDR' (if any)
    """
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR']
        return None