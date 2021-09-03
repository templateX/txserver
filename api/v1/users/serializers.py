from tags.models import Tag
from rest_framework import serializers
from accounts.models import User
from templates.models import Template, Repo
from follows.models import Follow


class UserTemplateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserTemplateRepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ('id', 'provider', 'url')


class UserTemplateSerializer(serializers.ModelSerializer):
    tags = UserTemplateTagSerializer(many=True, read_only=True)
    repos = UserTemplateRepoSerializer(many=True, read_only=True)

    class Meta:
        model = Template
        fields = ('id', 'title', 'slug', 'description', 'tags', 'repos')


class UserSerializer(serializers.ModelSerializer):
    templates = UserTemplateSerializer(many=True, read_only=True)
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'bio', 'profile_url', 'templates', 'following')

    def get_following(self, obj):
        if self.context['request'].user.id is not None:
            auth_user = self.context['request'].user
            try:
                Follow.objects.get(user=obj, follower=auth_user)
                return True
            except Follow.DoesNotExist:
                return False
        return False


class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'bio', 'profile_url')


class FollowSerializer(serializers.ModelSerializer):
    follower = FollowUserSerializer()

    class Meta:
        model = Follow
        fields = ('id', 'follower')
