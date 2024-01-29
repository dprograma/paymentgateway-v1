from django.urls import path
from . import consumers  

ws_urlpatterns = [
    path('ws/status/', consumers.StatusConsumer.as_asgi()),
]

