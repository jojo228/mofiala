from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Agence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.PositiveIntegerField(unique=True)
    nom_agence = models.CharField(max_length=200, null=True)
    date_creation = models.DateField(auto_now=True)

    def __str__(self):
        return self.nom_agence



class Contribuable(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    identity = models.CharField(max_length=200)
    nif = models.IntegerField(unique=True, null=True)
    denomination = models.CharField(max_length=200)
    is_owner = models.CharField(max_length=3)
    quarter = models.CharField(max_length=200)
    rue = models.CharField(max_length=200)
    door_number = models.CharField(max_length=20)
    parcel_number = models.CharField(max_length=20)
    lot_number = models.CharField(max_length=20)
    land_title_number = models.CharField(max_length=20)
    tel = models.CharField(max_length=12)
    longitude = models.CharField(max_length=200, blank=True)
    latitude = models.CharField(max_length=200, blank=True)
    geo_situation = models.CharField(max_length=200)
    photo_facade = models.ImageField(null=True, blank=True, upload_to="images")
    date = models.DateField(auto_now=True)


    def __str__(self):
        return self.first_name and self.last_name







