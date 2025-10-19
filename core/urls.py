# core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from tasks.views import UserViewSet, TaskViewSet, CategoryViewSet, TaskHistoryViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'task-history', TaskHistoryViewSet, basename='task-history')

@api_view(['GET'])
@permission_classes([AllowAny])
def public_api_root(request):
    return Response({
        'users': request.build_absolute_uri('/api/users/'),
        'tasks': request.build_absolute_uri('/api/tasks/'),
        'categories': request.build_absolute_uri('/api/categories/'),
        'task-history': request.build_absolute_uri('/api/task-history/'),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', public_api_root, name='public-api-root'),
    path('api-auth/', include('rest_framework.urls')),
]
