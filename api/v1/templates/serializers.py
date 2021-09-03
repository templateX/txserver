from rest_framework import serializers
from templates.models import Template, Repo, TemplateTag, Like
from tags.models import Tag
from accounts.models import User


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = ('id', 'name')


class TemplateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ('id', 'provider', 'url')


class TemplateTagSerializer(serializers.ModelSerializer):
    tag_name = serializers.SerializerMethodField(read_only=True)
    tag_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'tag_name', 'tag_id')

    def get_tag_name(self, obj):
        return obj.tag.name

    def get_tag_id(self, obj):
        return obj.tag.id


class TemplateSerializer(serializers.ModelSerializer):
    user = TemplateUserSerializer(read_only=True)
    template_tags = TemplateTagSerializer(many=True, read_only=False, required=False)
    tags = TagSerializer(many=True, write_only=True, required=False)
    repos = RepoSerializer(many=True, required=False)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = ('id', 'user', 'title', 'description', 'slug', 'preview_link', 'template_tags', 'tags', 'repos', 'liked', 'created_at')

    def get_liked(self, obj):
        if self.context['request'].user.id is not None:
            auth_user = self.context['request'].user
            try:
                Like.objects.get(template=obj, user=auth_user)
                return True
            except Like.DoesNotExist:
                return False
        return False

    def create(self, validated_data):
        tags = None
        repos = None

        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
        if 'repos' in validated_data:
            repos = validated_data.pop('repos')
        
        instance = super().create(validated_data)

        # Adding existing tags to repos
        if tags is not None:
            for tag in tags:
                t = Tag.objects.get(**tag)
                TemplateTag.objects.create(template=instance, tag=t)

        # Adding new repos
        if repos is not None:
            for repo in repos:
                Repo.objects.create(template=instance, **repo)

        return instance
