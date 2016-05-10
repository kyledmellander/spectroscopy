from django import forms

from .models import SignUp, Sample

class ContactForm(forms.Form):
    your_full_name = forms.CharField(required=True)
    your_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

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

class SearchForm(forms.Form):
    mineral_name = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Mineral Name'}))
    mineral_class = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Mineral Class'}))
    database_of_origin = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Database of origin'}))

