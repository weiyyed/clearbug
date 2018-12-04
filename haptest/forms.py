from django import forms

class AddProject(forms.Form):
    project_name=forms.CharField()

class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()