from django.urls import path
from . import views,fixture_manager
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('',views.index,name='index'),
    path('register_api',views.register_api,name='register_api'),
    path('edit_profile_api',views.edit_profile_api,name='edit_profile_api'),
    path('get_user_info',views.get_user_info,name='get_user_info'),
    path('login_api',views.login_api,name='login_api'),
    path('save_note',views.save_note,name='save_note'),
    path('logout_api',views.logout_api,name='logout_api'),
	path('register', views.register, name='register'),
    path('insert_metrics', views.insert_metrics, name='insert_metrics'),
    path('live_graph', views.live_graph, name='live_graph'),
    path('get_latest_metric', views.get_latest_value, name='get_latest_metric'),
    path('get_token', jwt_views.TokenObtainPairView.as_view(), name='get_token'),
    path('refresh_token', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
    path('auth_token', views.AuthView.as_view(), name='auth_token'),
]
try:
    fixture_manager.load_fixtures()
except Exception as e:
    print(e)
