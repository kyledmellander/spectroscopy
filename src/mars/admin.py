from django.contrib import admin
# Register your models here.
from mars.models import SignUp

class SignUpAdmin(admin.ModelAdmin):
	list_display = ('__str__','firstName','lastName')
	class Meta:
		model = SignUp

admin.site.register(SignUp,SignUpAdmin)