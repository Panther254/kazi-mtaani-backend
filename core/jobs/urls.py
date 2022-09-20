from django.urls import path
from .views import ListJobsView, PostJobView, PostedJobsView, RetrieveUpdateJob, JobsApplied, AcceptApplications, ApplyJob

urlpatterns = [
	path('list-available-jobs', ListJobsView.as_view()),
	path('post-job', PostJobView.as_view()),
	path('list-posted-jobs', PostedJobsView.as_view()),
	path('retrieve-update/<int:id>', RetrieveUpdateJob.as_view()),
	path('apply-job', ApplyJob.as_view()),
	path('list-applied-jobs', JobsApplied.as_view()),
	path('accept-applications/<int:id>', AcceptApplications.as_view()),
]