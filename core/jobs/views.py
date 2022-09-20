from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Job, JobApplied
from .serializers import JobSerializer, JobAppliedSerializer, UpdateJobAppliedSerializers, UsersJobSerializer
import random


# Create your views here.
class ListJobsView(APIView):
	serializer_class = UsersJobSerializer
	permission_classes = [permissions.AllowAny]

	def get(self,request,format=None):
		query = Job.objects.filter(is_available=True)
		jobs = UsersJobSerializer(query,many=True)

		return Response(jobs.data)


class PostJobView(generics.CreateAPIView):
	serializer_class = JobSerializer
	permission_classes = [permissions.IsAdminUser]

	def post(self,request,format=None):
		request.data._mutable=True
		data = self.request.data
		user_id = self.request.user.id
		data['posted_by'] = user_id
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

class PostedJobsView(generics.ListAPIView):
	serializer_class = JobSerializer
	permission_classes = [permissions.IsAdminUser]

	def get_queryset(self):
		queryset = Job.objects.filter(posted_by=self.request.user)
		return queryset

class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self,request,view, object):
		if request.method in permissions.SAFE_METHODS:
			return True

		return object.posted_by == request.user.id


class RetrieveUpdateJob(generics.RetrieveUpdateAPIView):
	serializer_class = JobSerializer
	permission_classes = [permissions.IsAdminUser&IsOwnerOrReadOnly]
	lookup_field = 'pk'
	queryset = Job.objects.all()

	
	def get_object(self):
		queryset = self.filter_queryset(self.get_queryset())
		obj = queryset.get(pk=self.kwargs['id'])
		return obj

class ApplyJob(generics.CreateAPIView):
	serializer_class = JobAppliedSerializer

	def post(self,request,*args,**kwargs):
		# request.data._mutable=True
		data = self.request.data
		user = self.request.user.id
		data['user'] = user
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		
		return Response(serializer.data,status.HTTP_202_ACCEPTED)


class JobsApplied(generics.ListAPIView):
	serializer_class = JobAppliedSerializer
	permission_classes = [permissions.IsAdminUser|IsOwnerOrReadOnly]

	def get_queryset(self):
		user = self.request.user
		queryset = JobApplied.objects.filter(user=user)
		return queryset


class AcceptApplications(APIView):
	permission_classes = [permissions.IsAdminUser]

	def get_random_applications(self,number_of_slots,*args,**kwargs):
		jobs_applications_id_list = JobApplied.objects.filter(job=kwargs['id']).values_list('id',flat=True)
		random_job_applications_id_list = random.sample(list(jobs_applications_id_list),min(len(jobs_applications_id_list),number_of_slots))
		queryset = JobApplied.objects.filter(id__in=random_job_applications_id_list)
		print("queryset:>>>>",queryset)
		return queryset

	def get(self,request,*args,**kwargs):
		job_id = kwargs['id']
		return Response({'job_id': job_id})

	def put(self,request,*args,**kwargs):
		data = self.request.data
		number_of_slots = data.pop('number_of_slots')
		queryset = self.get_random_applications(number_of_slots,**kwargs)
		instances = []
		for application in queryset.iterator():
			serializer = UpdateJobAppliedSerializers(application,data={'is_accepted': True },partial=True)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			instances.append(application)
		serializer = JobAppliedSerializer(instances,many=True)
		return Response(serializer.data)

	