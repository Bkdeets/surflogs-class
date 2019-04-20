from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'logs'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('<int:session_id>/session', views.detail, name='detail'),
    path('<int:report_id>/report', views.report, name='report'),
    path('profile/', views.profile, name='profile'),
    path('login_success/', views.profile, name='login_success'),
    path('profile/edit', views.profileEdit, name='profile_edit'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('feed/', views.feed, name='feed'),
    path('post_session/', views.post_session, name='post_session'),
    path('edit_session/<int:session_id>', views.edit_session, name='edit_session'),
    path('post_report/', views.post_report, name='post_report'),
    path('upload_photo/', views.upload_profile_pic, name='upload_photo'),
    path('signup/', views.signup, name='signup'),
    path('<str:username>/summary', views.user_summary, name='user_summary'),
    path('newspot/', views.create_spot, name='new_spot'),
    path('close/', views.autoclose, name='autoclose'),
    path('sessions/', views.session_list, name='session_list'),
    path('<str:spot_name>/spot', views.spot_view, name='spot_view'),
    path('session/<int:session_id>/upload_session_photos', views.add_photos, name='add_photos'),


]
