from django.shortcuts import render
from api.serializers import ShortTextSerializer
from .models import ShortText
from rest_framework import viewsets, permissions
from rest_framework.response import Response


# Create your views here.

class ShortTextViewSet(viewsets.ModelViewSet):
    queryset = ShortText.objects.all()
    serializer_class = ShortTextSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for shortText in queryset:
            shortText.viewcount += 1
            shortText.save()
        return super(viewsets.ModelViewSet, self).list(request, *args, **kwargs)
        # serializer = ShortTextSerializer(queryset, many=True)
        # return Response(serializer.data)
        
    def retrieve(self, request, *args, **kwargs):
        print('im here!')
        return super(viewsets.ModelViewSet, self).retrieve(request, *args, **kwargs)

