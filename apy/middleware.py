from django.utils.cache import add_never_cache_headers

class DisableBrowserCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Si el usuario cerró sesión o está autenticado,
        # le prohibimos al navegador guardar copias en el historial.
        add_never_cache_headers(response)
            
        return response