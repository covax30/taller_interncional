from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.views.generic import RedirectView 

#logica login 

class Login_view(LoginView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context ['titulo'] = 'Iniciar sesion'
        return context
    
#logout

class logoutredirect(RedirectView):
    pattern_name ='login'
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
