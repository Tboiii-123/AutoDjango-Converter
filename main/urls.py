from django.urls import path
from . import views

urlpatterns = [
    path('', views.convert_html, name='convert_html'),
]
