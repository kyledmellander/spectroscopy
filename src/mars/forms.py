from django import forms

from .models import Sample, SampleType

class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        # Due to issues with spaces, extra code has been added to reduce the list down
        # to ignore any extra spaces due to erroneous database entries
        dataBaseChoices = [c.strip() for c in Sample.objects.all().values_list('origin', flat=True).distinct()]
        dataBaseChoices = sorted(set(dataBaseChoices), key=lambda s: s.lower())
        dataBaseChoices = [(c, c) for c in dataBaseChoices]
        dataBaseChoices.insert(0, ('Any','Any'))

        allSampleTypes = [(c.strip(),c.strip()) for c in SampleType.objects.all().values_list('typeOfSample',flat=True).distinct()]
        allSampleTypes.insert(0, ('Any','Any'))

        print(dataBaseChoices)
        print(allSampleTypes)
        self.fields['database_of_origin'].choices = dataBaseChoices
        self.fields['type_of_sample'].choices = allSampleTypes

    mineral_name = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Gypsum','class':'autocomplete-name'}))
    mineral_class = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Sulfate','class':'autocomplete-class'}))
    mineral_Id= forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. ASD_SUL_21', 'class':'autocomplete-id'}))
    any_data = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    min_included_range = forms.IntegerField(required = False,
        widget = forms.NumberInput(), label='Min X (nm)')
    max_included_range = forms.IntegerField(required = False,
        widget = forms.NumberInput(), label='Max X (nm)')

    database_of_origin = forms.ChoiceField()
    type_of_sample = forms.ChoiceField()


class UploadFileForm(forms.Form):
    sample_class = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Sulfate'}))
    sample_type = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Tectosilicate'}))
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
