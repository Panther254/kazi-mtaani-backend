from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()




# Create your models here.
class Job(models.Model):
	FULL_TIME = "Full-time"
	PART_TIME = "Part-time"

	JOB_CHOICES = (
			(FULL_TIME,"Full time"),
			(PART_TIME, "Part time"),
		)

	posted_by = models.ForeignKey(User, related_name='jobs_applied',on_delete=models.CASCADE)
	position = models.CharField(max_length=255)
	job_type = models.CharField(max_length=20,choices=JOB_CHOICES,default=FULL_TIME)
	date_posted = models.DateField(max_length=255,auto_now_add=True)
	sector = models.CharField(max_length=255)
	location = models.CharField(max_length=255,default="Provide location")
	is_available = models.BooleanField(default=True)


	def __str__(self):
		return self.position


class JobApplied(models.Model):
	job = models.ForeignKey(Job,on_delete=models.CASCADE, related_name='applications')
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	date_applied = models.DateField(max_length=200,auto_now_add=True)
	is_accepted = models.BooleanField(default=False)


	def __str__(self):
		return self.user.email
