from django.urls import path, include
from .views import Login_view, logoutredirect

urlpatterns = [

    path('login/', Login_view.as_view(), name="login"),
    path('logout/', logoutredirect.as_view(), name="logout")
]