from rest_framework import serializers
from .models import Job, JobApplied


class JobSerializer(serializers.ModelSerializer):
	applications = serializers.StringRelatedField(many=True)
	class Meta:
		model = Job
		fields = '__all__'


class JobAppliedSerializer(serializers.ModelSerializer):
	class Meta:
		model = JobApplied
		fields = '__all__'