from django.contrib import admin
from django.urls import path,include
from apy.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apy/', include('apy.urls'))
]