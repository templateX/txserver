from re import template
from rest_framework import serializers
from templates.models import Template, Repo, Like, TemplateTag
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
        fields = ('id', 'provider', 'url')


# class TemplateSearchSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True)

#     class Meta:
#         model = Template
#         fields = ('title', 'tags',)


# class TemplateCreateSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     tags = TagSerializer(many=True, read_only=False)
#     repos = RepoSerializer(many=True, read_only=False)

#     class Meta:
#         model = Template
#         fields = ('id', 'user', 'title', 'description', 'slug', 'preview_link', 'tags', 'repos', 'created_at', 'updated_at')

#     def create(self, validated_data):
#         tags = validated_data.pop('tags')
#         repos = validated_data.pop('repos')

#         instance = super().create(validated_data)
#         for tag in tags:
#             t = Tag.objects.get(**tag)
#             TemplateTag.objects.create(template=instance, tag=t)

#         for repo in repos:
#             Repo.objects.create(template=instance, **repo)

#         return instance


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
    user = UserSerializer(read_only=True)
    template_tags = TemplateTagSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, write_only=True, required=False)
    repos = RepoSerializer(many=True, required=False)

    class Meta:
        model = Template
        fields = ('id', 'user', 'title', 'description', 'slug', 'preview_link', 'template_tags', 'tags', 'repos', 'created_at')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        repos = validated_data.pop('repos')
        instance = super().create(validated_data)

        # Adding Tags
        for tag in tags:
            t = Tag.objects.get(**tag)
            TemplateTag.objects.create(template=instance, tag=t)

        # Adding repos
        for repo in repos:
            Repo.objects.create(template=instance, **repo)

        return instance
