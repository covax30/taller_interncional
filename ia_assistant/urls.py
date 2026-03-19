from django.urls import path
from ia_assistant.view.views import api_consultar_ia

urlpatterns = [
    path('consultar/', api_consultar_ia, name='consultar_ia'),
]