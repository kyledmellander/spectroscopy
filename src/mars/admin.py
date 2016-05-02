from django.contrib import admin
# Register your models here.
from .models import Sample

class SampleAdmin(admin.ModelAdmin):
	list_display = ('data_id','sample_id','name','origin','sample_class','grain_size', 'refl_range')
	search_fields = ('data_id', 'sample_id', 'name', 'origin', 'sample_class', 'refl_range')

admin.site.register(Sample,SampleAdmin)
