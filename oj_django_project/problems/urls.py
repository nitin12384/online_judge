from django.urls import path
from . import views 

app_name = 'problems'

urlpatterns = [
    path('', views.index, name='index'),
    path('problem/<int:problem_id>', views.detail, name='detail_path'),
    path('submissions/<int:problem_id>', views.submissions_detail, name='submissions_detail_path')
]