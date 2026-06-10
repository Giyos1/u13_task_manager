from django.core.mail import send_mail
from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from tasks.models import Project, Task


class ProjectList(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    owner = UserSerializer()


class ProjectCreateAndUpdateSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=255)
    # description = serializers.CharField()
    # owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner')
        extra_kwargs = {'id': {'read_only': True}}

    def validate(self, data):
        name = data.get('name')
        description = data.get('description')

        if name == description:
            raise serializers.ValidationError('name va description bir xil bolishi mumkin emas')

        return data

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('name va minimum 3 carat')
        return value

    # def create(self, data):
    #     # name = data['name']
    #     # description = data['description']
    #     # project = Project.objects.create(name=name, description=description)
    #     # return project
    #     return Project.objects.create(**data)
    #
    # def update(self, instance, data):
    #     # name = data.get('name')
    #     # description = data.get('description')
    #     # instance.name = name
    #     # instance.description = description
    #     # instance.save()
    #     # return instance
    #     Project.objects.filter(id=instance.id).update(**data)
    #     return Project.objects.get(id=instance.id)


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', "description")


class TaskCreateAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', "to_user", "project","status")
        extra_kwargs = {'id': {'read_only': True}}
