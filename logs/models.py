from django.db import models
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from surflogs.storage_backends import PrivateMediaStorage
from PIL import Image



class Spot(models.Model):
    name =                  models.CharField(max_length=200, primary_key=True)
    ideal_tide =            models.CharField(max_length=200)
    ideal_wind_dir =        models.CharField(max_length=200)
    ideal_swell_dir	=       models.CharField(max_length=200)
    ideal_swell_height =    models.IntegerField(default=0)
    ideal_swell_period =    models.IntegerField(default=0)
    type =                  models.CharField(max_length=200)
    location =              models.CharField(max_length=200)
    description =           models.TextField(max_length=1000)

    def __str__(self):
        return self.name

class Wave_Data(models.Model):
    wave_data_id =  models.AutoField(primary_key=True)
    date =          models.DateField('date', default=timezone.now)
    time =          models.TimeField('time', default=timezone.now)
    spot =          models.ForeignKey(Spot, on_delete=models.CASCADE, default=1)
    tide =          models.CharField(max_length=200)
    crowd =         models.CharField(max_length=200)
    wind_dir =      models.CharField(max_length=200)
    wave_height =   models.IntegerField(default=0)
    wave_period =   models.CharField(max_length=200)
    wind_speed =    models.CharField(max_length=200)
    conditions =    models.CharField(max_length=200)


class Session_Record(models.Model):
    record_id =     models.AutoField(primary_key=True)
    user_id =       models.IntegerField(default=0)
    session_id =    models.IntegerField(default=0)
    datetime =      models.DateTimeField('date',default=timezone.now)

    def __str__(self):
        return str(user_id) + " " + str(session_id) +  " " + datetime



class Session(models.Model):
    session_id =     models.AutoField(primary_key=True)
    date =           models.DateTimeField('session date')
    start_time =     models.TimeField('start time')
    end_time = 	     models.TimeField('end time')
    wave_data =      models.ForeignKey(Wave_Data, on_delete=models.CASCADE)
    spot =           models.ForeignKey(Spot, on_delete=models.CASCADE, default=0)
    user =           models.ForeignKey(User, on_delete=models.CASCADE)
    notes =          models.TextField(max_length=500, blank=True)
    waves_caught = 	 models.IntegerField(default=0)
    rating =         models.IntegerField(default=0)

    def __str__(self):
        return "Session at " + self.spot.name + " from " + str(self.start_time) + " to " + str(self.end_time) + " on " + str(self.date.date()) + "."


class Profile(models.Model):
    user =          models.OneToOneField(User, on_delete=models.CASCADE)
    bio =           models.TextField(max_length=500, blank=True)
    homespot =      models.ForeignKey(Spot, on_delete=models.CASCADE, blank=True, null=True)
    photo =         models.FileField(storage=PrivateMediaStorage(), default='profile-photos/None/no-img.jpg')

    def __str__(self):
        return user.first_name + " " + user.last_name


class Report(models.Model):
    report_id =    models.AutoField(primary_key=True)
    date =         models.DateTimeField('date',default=timezone.now)
    time =         models.TimeField('time',default=timezone.now)
    spot =         models.ForeignKey(Spot, on_delete=models.CASCADE)
    user =         models.ForeignKey(User, on_delete=models.CASCADE)
    wave_data =    models.ForeignKey(Wave_Data, on_delete=models.CASCADE)
    notes =        models.TextField(max_length=500, blank=True)
    wave_quality = models.CharField(max_length=200)

    def __str__(self):
        return "Report: " + self.spot.name + " at " + str(self.date.date()) + "."


class Photo(models.Model):
    photo_id =          models.AutoField(primary_key=True)
    referencing_id =    models.IntegerField(null=True)
    image =             models.FileField(storage=PrivateMediaStorage(),default='photos/None/no-img.jpg')



class UserSummary(models.Model):
    user_id =       models.IntegerField(primary_key=True)
    username =      models.CharField(max_length=200)
    bio =           models.TextField(max_length=500, blank=True)
    homespot =      models.ForeignKey(Spot, on_delete=models.CASCADE, blank=True, null=True)
    photo =         models.FileField(upload_to='surflogs-photos', default='profile-photos/None/no-img.jpg')

    def __str__(self):
        return "User Summary: " + self.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def create_user_thumbnail(image):
    im = Image.open(image)
    w,h = im.size
    img_size = min(w,h)
    im = im.crop(box=(0,0, img_size, img_size))
    return im
