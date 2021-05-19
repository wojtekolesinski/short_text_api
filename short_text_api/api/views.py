from .serializers import ShortTextSerializer
from .models import ShortText
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend


class ShortTextViewSet(viewsets.ModelViewSet):
    queryset = ShortText.objects.all()
    serializer_class = ShortTextSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['viewcount', ]
    filterset_fields = {
        'viewcount': ['exact', 'gt', 'lt', 'gte', 'lte'],
        'text': ['contains'],
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
        return super(ShortTextViewSet, self).update(request, *args, **kwargs)

