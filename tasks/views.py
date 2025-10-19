from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from .models import Task, Category, TaskHistory
from .serializers import UserSerializer, TaskSerializer, CategorySerializer, TaskHistorySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date', 'category', 'recurring']
    ordering_fields = ['due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(
            models.Q(owner=self.request.user) | models.Q(shared_with=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except ValidationError as e:
            return Response({"detail": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            return Response({"detail": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        try:
            task.save()  # Recurring & history handled in model.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        task.status = 'pending'
        try:
            task.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

class TaskHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['completed_at', 'task', 'owner']
    ordering_fields = ['completed_at', 'logged_at']

    def get_queryset(self):
        return TaskHistory.objects.filter(owner=self.request.user).order_by('-completed_at')
