from django.db import models
from App_Login.models import Teacher,Student
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.db.models import signals
def upload_image(instance, filename):
    return "blog/{instance.blog_author.user.username}--{instance.blog_title}.png".format(instance=instance)

# Create your models here.
class Blog(models.Model):
    blog_title=models.CharField(max_length=300)
    blog_image=models.ImageField(upload_to=upload_image,blank=True)
    blog_author=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    slug=models.SlugField(max_length=264,unique=True,blank=True)
    blog_posted=models.DateTimeField(auto_now_add=True)
    blog_content=models.TextField(blank=True)
    class Meta:
        ordering=('-blog_posted',)
        verbose_name_plural='Article'
        db_table = 'Article'
    
    def __str__(self):
        return self.blog_title
    
    
@receiver(signals.pre_save, sender=Blog)
def populate_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.blog_title)
    
    
class Comments(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_comments')  
    commenter=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_comment')
    comment=models.TextField()
    comment_date=models.DateTimeField(auto_now_add=True)  
    class Meta:
        verbose_name_plural='Comment'
        db_table = 'Comment'
    
    def __str__(self):
        return self.comment