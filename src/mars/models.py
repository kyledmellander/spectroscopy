from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

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
	data_id = models.CharField(max_length=15)
	sample_id = models.CharField(max_length=20)
	date_accessed = models.DateTimeField(auto_now_add = False, auto_now = False)
	origin = models.CharField(max_length=50)
	locality = models.CharField(max_length=50, null=True, blank=True)
	name = models.CharField(max_length=100)
	sample_desc = models.CharField(max_length=500, null=True, blank=True)
	sample_type = models.CharField(max_length=100, null=True, blank=True)
	sample_class = models.CharField(max_length = 50, null=True, blank=True)
	grain_size = models.CharField(max_length=100, null=True, blank=True)
	view_geom = ArrayField(models.FloatField(), size=4, null=True, blank=True)
	resolution = ArrayField(models.FloatField(), size=4, null=True, blank=True)
	refl_range = ArrayField(models.FloatField(), size=2, null=True, blank=True)
	formula = models.CharField(max_length=20, null=True, blank=True)
	composition = models.CharField(max_length=1000, null=True, blank=True)
	reflectance = JSONField()
