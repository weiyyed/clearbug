from django import forms
from django.forms import ModelForm
from haptest.models import Project

class AddProjectForm(ModelForm):
    # project_name=forms.CharField(label='项目名称', max_length=20,)
    # platform=forms.CharField(label='平台', max_length=20,initial='prod3')
    class Meta:
        model=Project
        fields="__all__"


# class AddForm(forms.Form):
#     a = forms.IntegerField()
#     b = forms.IntegerField()