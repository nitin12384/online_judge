from django.urls import path
from . import views 

app_name = 'problems'

urlpatterns = [
    path('', views.index, name='index'),
    path('problem/<int:problem_id>', views.detail, name='detail_path'),
    path('submissions/<int:problem_id>', views.submissions_detail, name='submissions_detail_path'),
    path('submit/<int:problem_id>', views.submit_page, name='submit_page_path'),
    path('verdict/<int:submission_id>', views.get_verdict, name='check_verdict_path'),
    path('submit/', views.submit, name='submit_path') # for the post request
]