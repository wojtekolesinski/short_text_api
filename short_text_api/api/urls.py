from .views import ShortTextViewSet, RegisterView
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'shorttexts', ShortTextViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/register/', RegisterView.as_view(), name='register'),
]
