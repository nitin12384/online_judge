from django.urls import path
from . import views 

app_name = 'problems'

urlpatterns = [
    path('', views.index, name='index'),
    path('problem/<int:problem_id>', views.detail_submit, name='detail_submit_path'),
    path('submissions/<int:problem_id>', views.submissions_detail, name='submissions_detail_path'),
    
    path('profile/<str:username>', views.user_profile, name='user_profile_path'),
    
    path('submit/', views.submit, name='submit_path') # for the post request
]