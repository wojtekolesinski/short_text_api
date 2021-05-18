from django.shortcuts import render
from api import serializers
from .models import ShortText
from rest_framework import viewsets


# Create your views here.

class ShortTextViewSet(viewsets.ModelViewSet):
    queryset = ShortText.objects.all()
    serializer_class = serializers.ShortTextSerializer


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

