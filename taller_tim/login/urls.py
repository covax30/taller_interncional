from django.urls import path, include
from .views import Login_view, logout_redirect, forgot_view

app_name = 'login'
urlpatterns = [

    path('', Login_view.as_view(), name="login"),
    path('logout/', logout_redirect.as_view(), name="logout")
]