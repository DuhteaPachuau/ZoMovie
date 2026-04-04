class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options']  = 'nosniff'
        response['X-XSS-Protection']        = '1; mode=block'
        response['Referrer-Policy']         = 'strict-origin-when-cross-origin'
        response['Permissions-Policy']      = (
            'camera=(), microphone=(), geolocation=(), payment=(), usb=()'
        )
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https: blob:; "
            "frame-src https://www.youtube.com https://player.vimeo.com "
                       "https://iframe.mediadelivery.net https://streamable.com "
                       "https://odysee.com https://www.dailymotion.com; "
            "media-src 'none'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        if '/watch/' not in request.path:
            response['X-Frame-Options'] = 'SAMEORIGIN'

        if '/watch/' in request.path:
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
            response['Pragma']        = 'no-cache'

        return response