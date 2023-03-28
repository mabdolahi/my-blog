from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager , self).get_queryset().filter(status = 'published')

class Post(models.Model):
    STATUS = (
        ('published' , 'Published'),
        ('draft' , 'Draft')
    )
    title = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)
    body = models.TextField()
    author = models.ForeignKey(User , on_delete = models.CASCADE , related_name = 'blog_posts')
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 10 , choices = STATUS , default = 'draft')
    publish = models.DateTimeField(default = timezone.now)
    objects = models.Manager()


    class Meta:
        ordering = ('publish',)

    def get_absolute_url(self): #unique url for each post
        return reverse('blog:post_detail' , args = [self.slug])

    def __str__(self):
        return self.title

class Account(models.Model):
    GENDER = (
        ('آقا' , 'آقا'),
        ('خانم' , 'خانم')
    )
    user = models.OneToOneField(User , on_delete = models.CASCADE , related_name = 'account')
    phone = models.CharField(max_length = 11 , null = True , blank = True)
    gender = models.CharField(max_length = 5 , choices = GENDER , default = 'خانم')
    address = models.TextField(null = True , blank = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    age = models.PositiveIntegerField(default = 18 , blank = True , null = True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete = models.CASCADE , related_name = 'comments')
    name = models.CharField(max_length = 35)
    email = models.EmailField(null = True , blank = True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default = False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body , self.name)