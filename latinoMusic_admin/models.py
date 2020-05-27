from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from latinoMusic_app.models import (Song,Genre,Profile,SongPlay,Subscribers,Artist,Trending,Featured,Processed_payment,File_uploaded)


# Create your models here.
