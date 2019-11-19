from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
	path('register', views.register, name='register'),
    path('insert_metrics', views.insert_metrics, name='insert_metrics'),
    path('live_graph', views.live_graph, name='live_graph'),
    path('get_latest_metric', views.get_latest_value, name='get_latest_metric')
]
