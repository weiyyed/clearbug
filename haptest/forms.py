from django import forms

class AddProject(forms.Form):
    project_name=forms.CharField(label='项目名称', max_length=20,)
    platform=forms.CharField(label='平台', max_length=20,initial='prod3')

# class AddForm(forms.Form):
#     a = forms.IntegerField()
#     b = forms.IntegerField()