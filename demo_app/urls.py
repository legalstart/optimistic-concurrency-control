from django.urls import path

from . import views
from .rest.urls import api_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns = urlpatterns + api_urlpatterns
