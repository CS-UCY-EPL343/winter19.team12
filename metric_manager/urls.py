from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
	path('register', views.register, name='register'),
    path('insert_metrics', views.insert_metrics, name='insert_metrics')
]
