from django import forms

from .models import SignUp, Sample

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
