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

# def get_my_choices():
#     return choices_list

# class MineralForm(forms.Form):
    # mineral_name=forms.CharField()
    # def clean_mineral_name(self):
    #     try:
    #         mineral_name = int(self.cleaned_data["mineral_name"])
    #     except:
    #         mineral_name = None
    #
    #     if mineral_name and Sample.objects.filter(name=mineral_name).count:
    #         return mineral_name
    #     else:
    #         raise forms.ValidationError("Please enter a valid mineral name")
