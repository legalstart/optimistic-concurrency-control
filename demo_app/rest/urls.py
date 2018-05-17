from django.urls import re_path

from . import views

api_urlpatterns = [
    re_path(r'^api/document/(?P<pk>[0-9]+)',
         views.DocumentView.as_view(), name='document-endpoint'),
]
