from django.shortcuts import render
from . import models,serializers
from rest_framework import viewsets,generics,mixins,response
from App_Login.models import User,Teacher

# Create your views here.

class BlogSerializerView(viewsets.ModelViewSet):
    queryset=models.Blog.objects.all()
    serializer_class=serializers.BlogSerializer
    

class CommentSerializerView(viewsets.ModelViewSet):
    queryset=models.Comments.objects.all()
    serializer_class=serializers.CommentSerializer
    
    def create(self,request,*args,**kwargs):
        user=request.data['commenter']
        commenter=User.objects.get(username=user)
        blogy=request.data['blog']
        blog=models.Blog.objects.get(id=blogy)
        comment=request.data['comment']
        comments=models.Comments.objects.create(comment=comment,blog=blog,commenter=commenter)
        serializer=serializers.CommentSerializer(comments)
        return response.Response(serializer.data)
    
    
class BlogCreateSerializerView(generics.CreateAPIView):
    queryset=models.Blog.objects.all()
    serializer_class=serializers.BlogCreateSerializer
    def create(self,request,*args,**kwargs):
        print(request.data['blog_content'])
        user=request.data['blog_author']
        blog_author=Teacher.objects.get(user=user)
        blog_content=request.data['blog_content']
        blog_title=request.data['blog_title']
        blog_image=request.data['blog_image']
        blog=models.Blog.objects.create(blog_author=blog_author,blog_content=blog_content,blog_title=blog_title,blog_image=blog_image,slug=blog_title)
        serializer=serializers.BlogSerializer(blog,context={'request':request})
        return response.Response(serializer.data)
    
class BlogDetailSerializerView(generics.RetrieveAPIView):
    queryset=models.Blog.objects.all()
    serializer_class=serializers.BlogSerializer
    lookup_field='slug'
        