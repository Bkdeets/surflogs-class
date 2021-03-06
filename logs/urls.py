from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'logs'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('session/<int:session_id>', views.detail, name='detail'),
    path('report/<int:report_id>', views.report, name='report'),
    path('profile/', views.profile, name='profile'),
    path('login_success/', views.profile, name='login_success'),
    path('profile/edit', views.profileEdit, name='profile_edit'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('feed/', views.feed, name='feed'),
    path('post_session/', views.post_session, name='post_session'),
    path('edit_session/<int:session_id>', views.edit_session, name='edit_session'),
    path('edit_report/<int:report_id>', views.edit_report, name='edit_report'),
    path('post_report/', views.post_report, name='post_report'),
    path('upload_photo/', views.upload_profile_pic, name='upload_photo'),
    path('signup/', views.signup, name='signup'),
    path('<str:username>/summary', views.user_summary, name='user_summary'),
    path('newspot/', views.create_spot, name='new_spot'),
    path('close/', views.autoclose, name='autoclose'),
    path('sessions/', views.session_list, name='session_list'),
    path('<str:spot_name>/spot', views.spot_view, name='spot_view'),
    path('<int:referencing_id>/upload_photo/<is_session>', views.add_photos, name='add_photos'),
    path('<int:session_id>/delete_session/', views.delete_session, name='delete_session'),
    path('<int:report_id>/delete_report/', views.delete_report, name='delete_report'),
    path('search/Spot/<str:searchText>', views.spot_search, name='spot_search'),
    path('search/User/<str:searchText>', views.user_search, name='user_search'),
    path('search/Session/<str:searchText>', views.session_search, name='session_search'),
    path('search/Report/<str:searchText>', views.report_search, name='report_search'),

]
