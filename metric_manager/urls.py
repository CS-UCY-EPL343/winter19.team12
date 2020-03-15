from django.urls import path
from . import views,fixture_manager
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('',views.index,name='index'),
    path('register_api',views.register_api,name='register_api'),
    path('edit_profile_api',views.EditProfileApi.as_view(),name='edit_profile_api'),
    path('get_user_info',views.GetUserInfo.as_view(),name='get_user_info'),
    path('login_api',views.login_api,name='login_api'),
    path('logout_api',views.logout_api,name='logout_api'),
	path('retrieve_users', views.RetrieveUsers.as_view(), name='retrieve_users'),
	path('register', views.Register.as_view(), name='register'),
    path('get_specialist', views.GetSpecialist.as_view(), name='get_specialist'),
    path('insert_metrics', views.insert_metrics, name='insert_metrics'),
    path('retrieve_history_metrics',views.RetrieveHistoryMetrics.as_view(),name='retrieve_history_metrics'),
    path('retrieve_notes',views.RetrieveNotes.as_view(),name='retrieve_notes'),
    path('is_specialist',views.is_specialist,name='is_specialist'),
    path('save_note',views.SaveNotes.as_view(),name='save_note'),
    path('delete_note',views.DeleteNotes.as_view(),name='delete_note'),
    path('get_all_metrics',views.AllMetricsView.as_view(), name='get_all_metrics' ),
    path('live_graph', views.GraphView.as_view(), name='live_graph'),
    path('get_latest_metric', views.LatestValueView.as_view(), name='get_latest_metric'),
    path('user_latest_metric', views.UserLatestMetric.as_view(), name='user_latest_metric'),
    path('get_token', jwt_views.TokenObtainPairView.as_view(), name='get_token'),
    path('refresh_token', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
    path('auth_token', views.AuthView.as_view(), name='auth_token'),
    path('change_password', views.change_password, name='change_password'),
    path('permission_request', views.PermissionManager.as_view(), name='permission_request')
]
try:
    fixture_manager.load_fixtures()
except Exception as e:
    print(e)
