from django.urls import path
from . import views
from collections import Counter


urlpatterns = [
    path('create/',views.job_create,name='job_create'),
    path('student/view_jobs',views.view_all_students_jobs,name='view_jobs'),
    path('job/<int:id>/',views.job_detail,name='job_detail'),
    path('job_apply/<int:id>/',views.apply_job,name='apply_job'),
    path('recruiter/jobs/',views.recruiter_job,name='recruiter_jobs'),
    path('edit/<int:job_id>/',views.edit_job,name='edit_job'),
    path('delete/<int:job_id>/',views.delete_job,name='delete_job'),
    path('applicants/<int:job_id>/',views.view_applicants,name='view_applicants'),
    path('application/update/<int:application_id>/',views.update_application_status,name='update_application_status'),
]