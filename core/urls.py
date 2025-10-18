from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework import routers
from tasks.views import UserViewSet, TaskViewSet

# DRF router for users and tasks
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')

# Root URL redirects to /api/
def home(request):
    return redirect('/api/')

urlpatterns = [
    path('', home),  # Redirect root to API
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
