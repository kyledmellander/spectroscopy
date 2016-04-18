from django import forms

from .models import SignUp, Sample

class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ('firstName','lastName','email',)

    def clean_email(self):
    	cleaned = self.cleaned_data.get('email')
    	email_base, provider = cleaned.split('@')
    	domain, extension = provider.split('.')
    	if not "edu" in extension:
    		raise forms.ValidationError("Please use a valid .edu email address.")
    	return cleaned

# class MineralForm(forms.form):
#     mineral_name=forms.CharField()
#     def clean_mineral_name(self):
#         try:
#             mineral_name = int(self.cleaned_data["mineral_name"])
#         except:
#             mineral_name = None
#
#         if mineral_name and Sample.objects.filter(name=mineral_name).count:
#             return mineral_name
#         else:
#             raise forms.ValidationError("Please enter a valid mineral name")
