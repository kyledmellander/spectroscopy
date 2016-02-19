from django import forms

from .models import SignUp

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
