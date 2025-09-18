from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from login.views import forgot_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls'),name= 'login'),  # todas las rutas de tu app "login"
    path('apy/', include('apy.urls')),  # todas las rutas de tu app "apy"
    path('', forgot_view.as_view(), name="forgot"),

]

