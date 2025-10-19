from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Category, TaskHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    shared_with_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='shared_with',
        many=True,
        write_only=True,
        required=False
    )
    shared_with = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'due_date',
            'priority',
            'status',
            'completed_at',
            'category',
            'category_id',
            'recurring',
            'shared_with',
            'shared_with_ids'
        ]

class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = [
            'id',
            'task',
            'title',
            'description',
            'completed_at',
            'logged_at'
        ]
        read_only_fields = ['task', 'title', 'description', 'completed_at', 'logged_at']
