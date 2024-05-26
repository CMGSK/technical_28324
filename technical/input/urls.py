from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.get_data, name='result'),
    path('dashboard', views.index, name='index'),
    path('', views.insert_excel)
]
