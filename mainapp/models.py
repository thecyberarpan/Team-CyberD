from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class ContactMessage(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    subject = models.CharField(max_length = 150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.name
    

class Author(models.Model):
    Author_profile = models.ImageField(upload_to = 'AuthorImg/')
    Name = models.CharField(max_length=100, null=True)
    About_author = models.TextField()

    def __str__(self):
        return self.Name
    

class Blogpost(models.Model):
    UserId = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='Thumbnail/')
    slug = models.SlugField(max_length=500, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    


def create_slug(instance, new_slug = None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Blogpost.objects.filter(slug = slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug




def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect (pre_save_post_reciever, Blogpost)
