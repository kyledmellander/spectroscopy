from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models import Q
import json

#Create your models here.
class SignUp(models.Model):
  email = models.EmailField(primary_key=True)
  firstName = models.CharField(max_length = 120)
  lastName = models.CharField(max_length=120)
  timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
  updated = models.DateTimeField(auto_now_add = False, auto_now = True)

  def __str__(self):
    return self.emaills

class Sample(models.Model):
    data_id = models.CharField(max_length=15, unique=True, primary_key=True)
    sample_id = models.CharField(max_length=20)
    date_accessed = models.DateTimeField(auto_now_add = False, auto_now = False)
    origin = models.CharField(max_length=50)
    locality = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100)
    sample_desc = models.CharField(max_length=500, null=True, blank=True)
    sample_type = models.CharField(max_length=100, null=True, blank=True)
    sample_class = models.CharField(max_length = 50, null=True, blank=True)
    grain_size = models.CharField(max_length=100, null=True, blank=True)
    view_geom = models.CharField(max_length=50, null=True, blank=True)
    resolution = models.CharField(max_length=50, null=True, blank=True)
    refl_range = ArrayField(models.FloatField(), size=2, null=True, blank=True)
    formula = models.CharField(max_length=20, null=True, blank=True)
    composition = models.CharField(max_length=1000, null=True, blank=True)
    reflectance = JSONField(default = {})

    def as_dict(self):
        return {
        "data_id": self.data_id,
        "reflectance": self.reflectance,
        "sample_id" : self.sample_id,
        "origin" : self.origin,
        "locality" : self.locality,
        "name" : self.name,
        "sample_desc" : self.sample_desc,
        "sample_type" : self.sample_type,
        "sample_class" : self.sample_class,
        "grain_size" : self.grain_size,
        "view_geom" : self.view_geom,
        "resolution" : self.resolution,
        "refl_range" : self.refl_range,
        "formula" : self.formula,
        "composition" : self.composition,
        }


    @classmethod
    def create(cls, data_id, sample_id, date_accessed, origin, locality, name, sample_desc, sample_type, sample_class, grain_size, view_geom, resolution, refl_range, formula, composition, reflectance):
      sample = cls(data_id=data_id,sample_id=sample_id,date_accessed=date_accessed,origin=origin,locality=locality,name=name,sample_desc=sample_desc,sample_type=sample_type,sample_class=sample_class,grain_size=grain_size,view_geom=view_geom,resolution=resolution,refl_range=refl_range,formula=formula,composition=composition,reflectance=reflectance)
      return sample
