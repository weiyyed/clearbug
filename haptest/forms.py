from django.forms import ChoiceField, Select, Textarea
from django.forms import ModelForm,inlineformset_factory
from haptest.models import Project,Element,TestCase,CaseStep
from sweetest.config import web_keywords,common_keywords

class AddProjectForm(ModelForm):
    # project_name=forms.CharField(label='项目名称', max_length=20,)
    # platform=forms.CharField(label='平台', max_length=20,initial='prod3')
    class Meta:
        model=Project
        fields="__all__"
class AddElementForm(ModelForm):
    class Meta:
        model=Element
        fields="__all__"
class AddTestCaseForm(ModelForm):
    class Meta:
        model=TestCase
        fields="__all__"

class AddCaseStepForm(ModelForm):
    class Meta:
        model=CaseStep
        fields="__all__"
        keyword_pc=[]
        web_keywords.update(common_keywords)
        for k,v in web_keywords.items():
            if not k.isalpha:
                keyword_pc.append(k)
        widgets={
            'keyword':ChoiceField()
        }

CaseStepFormSet=inlineformset_factory(TestCase,CaseStep,form=AddCaseStepForm,fields=('id','no','keyword','page','element','data','output'),extra=1)