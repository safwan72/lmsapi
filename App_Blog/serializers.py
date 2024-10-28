from django.db.models import fields
from rest_framework import serializers
from . import models
class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

class CommentSerializer(serializers.ModelSerializer):
    commenter=StringSerializer()
    class Meta:
        model=models.Comments
        fields='__all__'
        depth=1

class BlogSerializer(serializers.ModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='blog_detail',read_only=True,lookup_field = 'slug')
    comments=serializers.SerializerMethodField()
    class Meta:
        model=models.Blog
        depth=1
        fields=(
            'id',
            'blog_title',
            'blog_image',
            'blog_author',
            'blog_posted',
            'blog_content',
            'url',
            'comments'
        )
    def get_comments(self,obj):
        comments=obj.blog_comments.all()
        return CommentSerializer(comments,many=True).data
        
class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Blog
        depth=1
        fields='__all__'