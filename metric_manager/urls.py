from django.urls import path
from . import views,fixture_manager
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('',views.index,name='index'),
    path('register_api',views.register_api,name='register_api'),
    path('edit_profile_api',views.edit_profile_api,name='edit_profile_api'),
    path('get_user_info',views.get_user_info,name='get_user_info'),
    path('login_api',views.login_api,name='login_api'),
    path('retrieve_notes',views.retrieve_notes,name='retrieve_notes'),
    path('retrieve_history_metrics',views.retrieve_history_metrics,name='retrieve_history_metrics'),
    path('save_note',views.save_note,name='save_note'),
    path('delete_note',views.delete_note,name='delete_note'),
    path('logout_api',views.logout_api,name='logout_api'),
	path('register', views.register, name='register'),
    path('insert_metrics', views.insert_metrics, name='insert_metrics'),
    path('get_metrics',views.get_metrics, name='get_metrics' ),
    path('get_all_metrics',views.AllMetricsView.as_view(), name='get_all_metrics' ),
    path('live_graph', views.GraphView.as_view(), name='live_graph'),
    path('get_latest_metric', views.LatestValueView.as_view(), name='get_latest_metric'),
    path('get_token', jwt_views.TokenObtainPairView.as_view(), name='get_token'),
    path('refresh_token', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
    path('auth_token', views.AuthView.as_view(), name='auth_token'),
    path('change_password', views.change_password, name='change_password')
]
try:
    fixture_manager.load_fixtures()
except Exception as e:
    print(e)
