from rest_framework import serializers
from .models import ShortText
from django.contrib.auth.models import User


class ShortTextSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    viewcount = serializers.ReadOnlyField()
    text_id = serializers.ReadOnlyField()

    class Meta:
        model = ShortText
        fields = ['text_id', 'title', 'text', 'viewcount']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets', 'email']