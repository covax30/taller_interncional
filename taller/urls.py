from django.contrib import admin
from django.urls import path, include
from login.views import forgot_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include(('login.urls', 'login'), namespace='login')),  # ✅ con namespace
    path('apy/', include(('apy.urls', 'apy'), namespace='apy')),          # idem, por claridad
    path('forgot/', forgot_view.as_view(), name="forgot"),
]
