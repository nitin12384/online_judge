from django.urls import path
from . import views 

app_name = 'problems'

urlpatterns = [
    path('', views.index, name='index'),
    path('problem/<int:problem_id>', views.detail_submit, name='detail_submit_path'),
    path('submissions/<int:problem_id>', views.submissions_detail, name='submissions_detail_path'),
    
    path('profile/<str:username>', views.user_profile, name='user_profile_path'),
    
    path('submit/', views.submit, name='submit_path'), # for the post request

    ## Auth urls
    path('login_page/', views.login_page, name='login_page_path'),
    path('signup_page/', views.signup_page, name='signup_page_path'),
    
    ## Auth actions urls for post request
    path('login_action', views.login_action, name='login_action_path'),
    path('signup_action', views.signup_action, name='signup_action_path'),
    path('logout_action', views.logout_action, name='logout_action_path'),
]