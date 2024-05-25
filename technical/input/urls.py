from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.result, name='result'),
    path('', views.index, name='index')
]
