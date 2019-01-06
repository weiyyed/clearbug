from django.db import models


class Base(models.Manager):
    # 获取字典列表，[{field:vlaue},{}]
    def get_dicts(self,id):
        obj=self.model()
        return  [m for m in obj.objects.filter(pk=id).values_list()]


class TestCaseManager(Base):
    def get_testcases(self):
        obj=self.model()
        obj.objects.filter()
class CaseStepManager(Base):
    pass
class ElementManager(Base):
    pass
class RunCaseManager(Base):
    def get_testcases(self,id):
        obj=self.model()
        r=obj.objects.get(pk=id)
        modules=r.module.all()
        return r.plateform.testcase_set.all().filter(module_name__in=modules)