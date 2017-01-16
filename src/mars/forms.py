from django import forms

from .models import Sample

class SearchForm(forms.Form):
    mineral_name = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Gypsum'}))
    mineral_class = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Sulfate'}))
    mineral_Id= forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. ASD_SUL_21'}))
    database_of_origin = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['database_of_origin'].choices = [(c, c) for c in Sample.objects.all().values_list('origin', flat=True).distinct()]
        # Allow any database to be selected
        self.fields['database_of_origin'].choices.insert(0, ('Any','Any'))

class UploadFileForm(forms.Form):
    sample_class = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Sulfate'}))
    sample_type = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Tectosilicate'}))
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
