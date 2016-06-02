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
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Gypsum'}))
    mineral_class = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Sulfate'}))
    mineral_Id= forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g. ASD_SUL_21'}))
    querylist=list(Sample.objects.all().values_list('origin', flat=True).distinct())
    querylist=list(map(str, querylist))
    for i in range(len(querylist)):
        querylist[i] = (querylist[i], querylist[i])
    querylist.insert(0, ('Any', 'Any'))
    database_of_origin = forms.ChoiceField(choices=querylist)

class UploadFileForm(forms.Form):
    sample_class = forms.CharField(required=False,
      widget=forms.TextInput(attrs={'placeholder': 'e.g. Sulfate'}))
    sample_type = forms.CharField(required=False,
      widget=forms.TextInput(attrs={'placeholder': 'e.g. Tectosilicate'}))
    file = forms.FileField()

