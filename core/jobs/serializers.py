from dataclasses import fields
from rest_framework import serializers
from .models import Job, JobApplied


class JobSerializer(serializers.ModelSerializer):
	applications = serializers.StringRelatedField(many=True)
	class Meta:
		model = Job
		fields = '__all__'
		read_only_fields = ["applications"]
		extra_kwargs = {
			'applications':{ 'required': False, 'allow_blank': True, 'allow_null': True},
		}


class JobAppliedSerializer(serializers.ModelSerializer):
	class Meta:
		model = JobApplied
		fields = '__all__'
		read_only_fields = ['is_accepted']

class UpdateJobAppliedSerializers(serializers.ModelSerializer):
	class Meta:
		model = JobApplied
		fields = '__all__'

class UsersJobSerializer(serializers.ModelSerializer):
	# applications = serializers.StringRelatedField(many=True)
	class Meta:
		model = Job
		fields = '__all__'
		# exclude = ['applications']

