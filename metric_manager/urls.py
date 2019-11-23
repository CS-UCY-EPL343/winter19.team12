from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register_api',views.register_api,name='register_api'),
    path('edit_profile_api',views.edit_profile_api,name='edit_profile_api'),
    path('get_user_info',views.get_user_info,name='get_user_info'),
    path('login_api',views.login_api,name='login_api'),
    path('logout_api',views.logout_api,name='logout_api'),
	path('register', views.register, name='register'),
    path('insert_metrics', views.insert_metrics, name='insert_metrics'),
    path('live_graph', views.live_graph, name='live_graph'),
    path('get_latest_metric', views.get_latest_value, name='get_latest_metric')
]
