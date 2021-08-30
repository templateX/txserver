from tags.models import Tag
from rest_framework import serializers
from accounts.models import Follow, User
from templates.models import Template, Repo


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ('id', 'provider', 'link')


class TemplateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    repos = RepoSerializer(many=True, read_only=True)

    class Meta:
        model = Template
        fields = ('id', 'title', 'slug', 'description', 'tags', 'repos')


class UserSerializer(serializers.ModelSerializer):
    templates = TemplateSerializer(many=True, read_only=True)
    followers_count = serializers.ReadOnlyField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'bio', 'profile_url', 'followers_count', 'following', 'templates')

    def get_following(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            try:
                user.followings.get(user=obj)
                return True
            except Follow.DoesNotExist:
                return False
        else:
            return False
