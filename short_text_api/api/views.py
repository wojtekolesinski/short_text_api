from .serializers import ShortTextSerializer, RegisterSerializer
from .models import ShortText
from rest_framework import viewsets, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User


class RegisterView(generics.CreateAPIView):
    """
    View for user registrations, accepts only POST, and OPTIONS
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class ShortTextViewSet(viewsets.ModelViewSet):
    """
    Main API view, accepts OPTIONS, GET requests (from everyone)
    as well as POST, PUT, DELETE from authenticated users only
    """
    queryset = ShortText.objects.all()
    serializer_class = ShortTextSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'viewcount': ['exact', 'gt', 'lt', 'gte', 'lte'],
        'text': ['exact', 'contains'],
    }

    def list(self, request, *args, **kwargs):
        for shortText in self.get_queryset():
            shortText.viewcount += 1
            shortText.save()
        return super(viewsets.ModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        text = self.get_object()
        text.viewcount += 1
        text.save()
        return super(viewsets.ModelViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        text = self.get_object()
        text.viewcount = 0
        text.save()
        return super(viewsets.ModelViewSet, self).update(request, *args, **kwargs)
