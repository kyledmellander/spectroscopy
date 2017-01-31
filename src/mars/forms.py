from django import forms

from .models import Sample

class SearchForm(forms.Form):
    mineral_name = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Gypsum'}))
    mineral_class = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Sulfate'}))
    mineral_Id= forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. ASD_SUL_21'}))
    any_data = forms.BooleanField(required=False)
    min_included_range = forms.IntegerField(required = False,
        widget = forms.NumberInput(), label='Min X (nm)')
    max_included_range = forms.IntegerField(required = False,
        widget = forms.NumberInput(), label='Max X (nm)')

    database_of_origin = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        # Due to issues with spaces, extra code has been added to reduce the list down
        # to ignore any extra spaces due to erroneous database entries
        dataBaseChoices = [c.strip() for c in Sample.objects.all().values_list('origin', flat=True).distinct()]
        dataBaseChoices = sorted(set(dataBaseChoices), key=lambda s: s.lower())
        dataBaseChoices = [(c, c) for c in dataBaseChoices]
        dataBaseChoices.insert(0, ('Any','Any'))

        self.fields['database_of_origin'].choices = dataBaseChoices

class UploadFileForm(forms.Form):
    sample_class = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Sulfate'}))
    sample_type = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Tectosilicate'}))
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
