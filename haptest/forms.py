from django.forms import ChoiceField, Textarea, Select
from django.forms import ModelForm, inlineformset_factory
from haptest.models import Project, Element, TestCase, CaseStep, RunCase, Environment, Data
from sweetest.config import web_keywords, common_keywords
# from django import forms

class AddProjectForm(ModelForm):
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
        keyword_pc=[('',"---")]
        web_keywords.update(common_keywords)
        for k,v in web_keywords.items():
            if not k.isupper():
                keyword_pc.append((v,k))
        page_set= Element.objects.get_page_tuples()
        ele_set=Element.objects.get_element_tuples()
        ele_set.extend(TestCase.objects.get_snippet_tuples())
        widgets={
            'keyword':Select(choices=keyword_pc),
            'page':Select(choices=page_set,attrs={'onchange':'change_element(this.id)'}),
            'element':Select(choices=ele_set)
        }

def get_CaseStepFormSet(extra=0):
    # 用例步骤
    return inlineformset_factory(TestCase, CaseStep, form=AddCaseStepForm,
                                        fields=('id', 'no', 'keyword', 'page', 'element',"ele_parameter", 'data', 'output'), extra=extra,can_delete=True)

class RunCaseForm(ModelForm):
    class Meta:
        model = RunCase
        fields = "__all__"

class AddEnvironmentForm(ModelForm):
    # 环境信息
    class Meta:
        model = Environment
        fields = "__all__"
class DataForm(ModelForm):

    class Meta:
        model = Data
        fields = "__all__"