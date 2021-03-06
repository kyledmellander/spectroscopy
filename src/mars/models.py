from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models import Q
import json

#Create your models here.
class About(models.Model):
    html = models.TextField(blank=False)
    position = models.IntegerField()

    def __str__(self):
        return "About HTML Entry - " + str(self.position)

    def position_display(self):
        return str(self)

    class Meta:
        ordering = ['position']
        verbose_name= "About Entry"
        verbose_name_plural= "About Entries"


class Database(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    position = models.IntegerField(default=1)

    class Meta:
        ordering = ['position', 'name']

    def __str__(self):
        return self.name + ", <" + self.url + ">"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        if self.url:
            self.url = self.url.strip()
        if self.description:
            self.description = self.description.strip()
        super(Database, self).save(*args, **kwargs)

class SampleType(models.Model):
    typeOfSample = models.CharField(verbose_name='Type Of Sample', max_length=20, unique=True, primary_key=True, blank=False)

    class Meta:
        verbose_name= "Sample Type"
        verbose_name_plural= "Sample Types"

    def __str__(self):
        return self.typeOfSample

class File(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

class Sample(models.Model):
    data_id = models.CharField(max_length=20, unique=True, primary_key=True)
    sample_id = models.CharField(max_length=30)
    date_added = models.DateTimeField(auto_now=True)
    origin = models.CharField(max_length=100)
    locality = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    sample_desc = models.TextField(null=True, blank=True)
    mineral_type = models.CharField(max_length=50, null=True, blank=True)
    sample_class = models.CharField(max_length=50, null=True, blank=True)
    grain_size = models.CharField(max_length=50, null=True, blank=True)
    view_geom = models.CharField(max_length=50, null=True, blank=True)
    resolution = models.CharField(max_length=30, null=True, blank=True)
    refl_range = ArrayField(models.FloatField(), size=2, null=True, blank=True)
    formula = models.CharField(max_length=50, null=True, blank=True)
    composition = models.CharField(max_length=1000, null=True, blank=True)
    reflectance = JSONField(default = {})
    sample_type = models.ForeignKey(SampleType, null=True,)
    references = models.TextField(null=True, blank=True)
    other = models.TextField(null=True, blank=True)
    flagged = models.PositiveIntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        if float(self.refl_range[0]) < 0:
            minReflectance = float('inf')
            maxReflectance = -1.0
            invalid = list()

            for (key, value) in self.reflectance.iteritems():
                print(key, value)

                if (float(key) < 0 or float(value) < 0):
                    invalid.append(key)
                else:
                    if (float(key) < minReflectance):
                        minReflectance = float(key)
                    if (float(key) > maxReflectance):
                        maxReflectance = float(key);

            # Remove invalid values
            for (key) in invalid:
                self.reflectance.pop(key)

            # Update refl_range
            self.refl_range[0] = minReflectance
            self.refl_range[1] = maxReflectance

        super(Sample, self).save(*args, **kwargs)

    def as_dict(self):
        return {
        "data_id": self.data_id,
        "reflectance": self.reflectance,
        "sample_id" : self.sample_id,
        "origin" : self.origin,
        "locality" : self.locality,
        "name" : self.name,
        "sample_desc" : self.sample_desc,
        "mineral_type" : self.mineral_type,
        "sample_class" : self.sample_class,
        "grain_size" : self.grain_size,
        "view_geom" : self.view_geom,
        "resolution" : self.resolution,
        "refl_range" : self.refl_range,
        "formula" : self.formula,
        "composition" : self.composition,
        "references" : self.references,
        "other" : self.other,
        }

    class Meta:
        verbose_name = "Sample"
        verbose_name_plural = "Samples"

    def __str__(self):
        return self.data_id

class TeamMember(models.Model):
    name = models.CharField(max_length=30, blank=False)
    role = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    position = models.IntegerField(default=1)
    image = models.ImageField(upload_to = 'pic_folder/', blank=True)

    class Meta:
        ordering = ['position','name']
        verbose_name= "Team Member"
        verbose_name_plural= "Team Members"

    def __str__(self):
        return "Team Member: " + self.name

    def position_display(self):
        return "Ordering Position: " + str(self.position)
