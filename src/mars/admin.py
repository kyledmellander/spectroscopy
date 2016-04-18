from django.contrib import admin
# Register your models here.
from .models import Sample

class SampleAdmin(admin.ModelAdmin):
	list_display = ('data_id','sample_id','origin','sample_class','grain_size')

admin.site.register(Sample,SampleAdmin)
