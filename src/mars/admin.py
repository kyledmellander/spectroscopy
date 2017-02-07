from django.contrib import admin
# Register your models here.
from .models import Sample, SampleType, Database

# Allow Admin Users to set the type of multiple Samples at once
def MarkAsMineralType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Mineral'))

MarkAsMineralType.short_description = "Mark selected samples as Minerals"

class SampleTypeAdmin(admin.ModelAdmin):
    list_display = ('typeOfSample',)

class SampleAdmin(admin.ModelAdmin):
    actions = [MarkAsMineralType];
    list_display = ('data_id','sample_id','name','date_added','origin','sample_class','grain_size', 'refl_range')
    readonly_fields = ('date_added',)
    search_fields = ('data_id', 'sample_id', 'name', 'origin', 'sample_class', 'refl_range')

class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name','url')
    search_fields = ('name', 'url')

admin.site.register(SampleType,SampleTypeAdmin)
admin.site.register(Sample,SampleAdmin)
admin.site.register(Database,DatabaseAdmin)
#admin.site.register(DataFile)
