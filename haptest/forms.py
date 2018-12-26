from django.forms import ChoiceField, Textarea, Select
from django.forms import ModelForm, inlineformset_factory
from haptest.models import Project, Element, TestCase, CaseStep
from sweetest.config import web_keywords, common_keywords
# from django import forms


class AddProjectForm(ModelForm):
    # project_name=forms.CharField(label='项目名称', max_length=20,)
    # platform=forms.CharField(label='平台', max_length=20,initial='prod3')
    class Meta:
        model = Project
        fields = "__all__"


class AddElementForm(ModelForm):
    class Meta:
        model = Element
        fields = "__all__"


class AddTestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        fields = "__all__"


class AddCaseStepForm(ModelForm):
    class Meta:
        model=CaseStep
        fields="__all__"
        keyword_pc=[]
        web_keywords.update(common_keywords)
        for k,v in web_keywords.items():
            if not k.isupper():
                keyword_pc.append((v,k))
        page_set=[]
        for x in Element.objects.values('page').distinct():
            page_set.append((x['page'],x['page']))
        widgets={
            'keyword':Select(choices=keyword_pc),
            'page':Select(choices=page_set)
        }

CaseStepFormSet = inlineformset_factory(TestCase, CaseStep, form=AddCaseStepForm,
                                        fields=('id', 'no', 'keyword', 'page', 'element', 'data', 'output'), extra=1)
