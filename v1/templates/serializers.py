from re import template
from rest_framework import serializers
from templates.models import Template, Repo
from tags.models import Tag
from accounts.models import User


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ('id', 'provider', 'link')


class TemplateSearchSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = Template
        fields = ('title', 'tags', 'like_count')


class TemplateCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=False)
    repos = RepoSerializer(many=True, read_only=False)

    class Meta:
        model = Template
        fields = ('id', 'user', 'title', 'description', 'slug', 'preview_link', 'tags', 'repos', 'created_at', 'updated_at')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        repos = validated_data.pop('repos')

        instance = super().create(validated_data)
        for tag in tags:
            instance.tags.add(Tag.objects.get(**tag))

        for repo in repos:
            Repo.objects.create(template=instance, **repo)

        return instance


class TemplateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = Template
        fields = ('id', 'user', 'title', 'description', 'slug', 'preview_link', 'tags', 'like_count', 'created_at', 'updated_at')
