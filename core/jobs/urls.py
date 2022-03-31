from django.urls import path
from .views import ListJobsView, PostJobView, RetrieveUpdateJob, JobsApplied

urlpatterns = [
	path('list-jobs', ListJobsView.as_view()),
	path('post-job', PostJobView.as_view()),
	path('retrieve-update/<int:id>', RetrieveUpdateJob.as_view()),
	path('apply-job', JobsApplied.as_view()),
]