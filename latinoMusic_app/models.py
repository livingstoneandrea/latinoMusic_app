from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True,null=True)
    first_name = models.CharField(max_length=100, blank=True,null=True)
    last_name = models.CharField(max_length=100, blank=True,null=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
class Genre(models.Model):
    genre = models.CharField(max_length=120)
    genre_image = models.ImageField(upload_to='artists_rep',blank=True)
    genre_description = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.genre   
class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True,blank=True)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to ='profile_pics',blank=True) 
    
    def __str__(self):
        return self.name       
     
class Song(models.Model):
    title = models.CharField(max_length=100)
    track = models.FileField(upload_to='audio',blank=True)
    artist_image = models.ImageField(upload_to='artists_rep',blank=True,null=True)
    genreid = models.ForeignKey(Genre,on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE,null=True,blank=True)
    year = models.DateTimeField(null=True,blank=True,default=timezone.now)
    duration = models.DurationField(null=True)
    def __str__(self):
        return self.title
class Trending(models.Model):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    time = models.DateTimeField(default = timezone.now)      
    def __str__(self):
        return self.song.title
class Featured(models.Model):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    time = models.DateTimeField(default = timezone.now)      
    def __str__(self):
        return self.song.title    
class PlayList(models.Model):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    time = models.DateTimeField(default = timezone.now)      
    def __str__(self):
        return self.song.title       
class SongPlay(models.Model):
    start_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    songid = models.ForeignKey(Song,on_delete=models.CASCADE)
    
    def __str(self):
        return self.songid.title
           
class Processed_payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=60)
    paid = models.BooleanField(default=False)
    total_paid = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
     
    def __str__(self):
        return self.user_id
class Subscribers(models.Model):
    email = models.EmailField(max_length=100,unique=True)
    def __str__(self):
        return self.email
class Testimonial(models.Model):
    name = models.CharField(max_length=120,blank=True)
    occupation = models.CharField(max_length=60,blank=True)
    profile_pic = models.ImageField(upload_to='testimonials',blank=True)
    comment = models.TextField()
    def __str__(self):
        return self.name      
class File_uploaded(models.Model):
    track_title = models.CharField(max_length=250,blank=True)
    track = models.FileField(upload_to='audio/',blank=True)
    submitted_date = models.DateTimeField(default=timezone.now)
    comments = models.TextField()

    def __str__(self):
        return self.track_title
    