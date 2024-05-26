from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.get_data_from_epoch, name='result'),
    path('dashboard/', views.index, name='index'),
    path('dashboard/<int:id>', views.get_data_from_epoch, name='getdata'),
    path('', views.insert_excel)
]
