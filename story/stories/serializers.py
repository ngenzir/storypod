from django.conf import settings
from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import Story

MAX_STORY_LENGTH = settings.MAX_STORY_LENGTH
STORY_ACTION_OPTIONS = settings.STORY_ACTION_OPTIONS

class StoryActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in STORY_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for stories")
        return value


class StoryCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True) # serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Story
        fields = ['user', 'id', 'content', 'likes', 'timestamp']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):
        if len(value) > MAX_STORY_LENGTH:
            raise serializers.ValidationError("This story is too long")
        return value

    # def get_user(self, obj):
    #     return obj.user.id


class StorySerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    parent = StoryCreateSerializer(read_only=True)
    class Meta:
        model = Story
        fields = [
                'user', 
                'id', 
                'content',
                'likes',
                'is_restory',
                'parent',
                'timestamp']

    def get_likes(self, obj):
        return obj.likes.count()
