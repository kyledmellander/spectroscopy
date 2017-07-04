from django.contrib import admin
# Register your models here.
from .models import About, Database, File, Sample, SampleType, TeamMember

# Allow Admin Users to set the type of multiple Samples at once
def MarkAsMineralType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Mineral'))

def MarkAsMixtureType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Mixture'))

def MarkAsCoatingType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Coating'))

def MarkAsVolatileType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Volatile'))

def MarkAsRockType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Rock'))

def MarkAsDustCoatingType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Dust Coating'))

def MarkAsMeteoriteType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Meteorite'))

def Update(modelAdmin, request, queryset):
    for sample in queryset:
        sample.save()

def MarkAsWholeRockType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Whole Rock'))

def MarkAsOtherType(modelAdmin, request, queryset):
    queryset.update(sample_type=SampleType.objects.get(pk='Other'))

MarkAsMixtureType.short_description = "Mark selected samples as Mixture"
MarkAsMineralType.short_description = "Mark selected samples as Minerals"
MarkAsCoatingType.short_description = "Mark selected samples as Coating"
MarkAsVolatileType.short_description = "Mark selected samples as Volatile"
MarkAsRockType.short_description = "Mark selected samples as Rock"
MarkAsDustCoatingType.short_description = "Mark selected samples as Dust Coating"
MarkAsMeteoriteType.short_description = "Mark selected samples as Meteorite"
MarkAsWholeRockType.short_description = "Mark selected samples as Whole Rock"
MarkAsOtherType.short_description = "Mark selected samples as Other"
Update.short_description = "Resave / auto format data"


class AboutAdmin(admin.ModelAdmin):
    list_display = ('position_display',)

class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name','url')
    search_fields = ('name', 'url')

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_uploaded')

class SampleTypeAdmin(admin.ModelAdmin):
    list_display = ('typeOfSample',)

class SampleAdmin(admin.ModelAdmin):
    actions = [Update,MarkAsMineralType, MarkAsMixtureType, MarkAsCoatingType, MarkAsVolatileType, MarkAsRockType, MarkAsDustCoatingType, MarkAsMeteoriteType, MarkAsWholeRockType, MarkAsOtherType];
    list_display = ('data_id','sample_id','name','date_added','flagged','sample_type','origin','sample_class','grain_size', 'refl_range')
    readonly_fields = ('date_added',)
    search_fields = ('data_id', 'sample_id', 'name', 'origin','sample_type__typeOfSample','sample_class', 'refl_range')

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name','role', 'position_display',)


admin.site.register(About, AboutAdmin)
admin.site.register(Database,DatabaseAdmin)
admin.site.register(SampleType,SampleTypeAdmin)
admin.site.register(Sample,SampleAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(TeamMember,TeamMemberAdmin)
