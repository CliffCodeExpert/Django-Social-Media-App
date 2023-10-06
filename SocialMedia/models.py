from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
import uuid
from datetime import datetime

User = get_user_model()
# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE) 
  follows = models.ManyToManyField("self",
             related_name="followed_by",
             symmetrical=False,
             blank=True)  
  bio = models.TextField(blank=True)
  profileimg = models.ImageField(upload_to='profile_images',default='blank.jpg',blank=True,null=True)
  location = models.CharField(max_length=100,blank=True)


  def __str__(self):
    return self.user.username
  

# Create Profile When New User Signs Up
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.add(user_profile)
        user_profile.save()

post_save.connect(create_profile,sender=User)

class Post(models.Model):
   id = models.UUIDField (primary_key=True,default=uuid.uuid4)
   user = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
   image = models.ImageField(upload_to='post_images')
   caption = models.TextField()
   created_at = models.DateTimeField(default=datetime.now)
   no_of_likes = models.IntegerField(default=0)

   def __str__(self):
      return self.user.username
   
class LikePost(models.Model):
   post_id= models.CharField(max_length=500)
   username = models.CharField(max_length=100)


   def __str__(self):
      return self.username
