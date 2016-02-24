from django.contrib import admin
# Register your models here.
from .forms import SignUpForm
from .models import SignUp
from .models import Sample

class SignUpAdmin(admin.ModelAdmin):
	list_display = ('__str__','firstName','lastName')
	form = SignUpForm
	#class Meta:
		#model = SignUp

class SampleAdmin(admin.ModelAdmin):
	list_display = ('data_id','sample_id','date_accessed','view_geom')

admin.site.register(Sample,SampleAdmin)
