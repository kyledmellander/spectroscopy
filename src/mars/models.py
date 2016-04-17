from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models import Q

#Create your models here.
class SignUp(models.Model):
	email = models.EmailField(primary_key=True)
	firstName = models.CharField(max_length = 120)
	lastName = models.CharField(max_length=120)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True)

	def __str__(self):
		return self.emaills

class SampleManager(models.Manager):
	def search(self, search_terms):
		terms = [term.strip() for term in search_terms.split()]
		q_objects = []

		for term in terms:
			q_objects.append(Q(title__icontains=term))
			q_objects.append(Q(content__icontains=term))

		#start with bare QuerySet
		qs=self.get_query_set()

		#use operator's or_ to string together all of your Q objects
		return qs.filter(reduce(operator.or_, q_objects))



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
	objects = SampleManager()
