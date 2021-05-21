from .views import ShortTextViewSet, RegisterView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'shorttexts', ShortTextViewSet)
import rest_framework.urls
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/register/', RegisterView.as_view(), name='register'),
]
