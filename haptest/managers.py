from django.db import models


class Base(models.Manager):
    # 获取字典列表，[{field:vlaue},{}]
    def get_dicts(self,**kwargs):

        # obj=self.model()
        return  [m for m in super().filter(**kwargs).values()]


class DataManager(Base):
    def get_dict(self,**kwargs):
        # 获取第一条未使用数据
        d=super().filter(**kwargs)
        if d:
            data_first=d.exclude(flag="Y")[:1]
            d_dicts=data_first.values()[:1]
            new_dic = {}
            if d_dicts:
                # 重置为N
                d_dicts=[d for d in d_dicts]
                super().filter(pk=data_first.get().id).update(flag="Y")
                verbose_dic=self.get_verbose_dic()
                for name,vername in verbose_dic.items():
                    new_dic[vername]=d_dicts[0][name]
                return new_dic
            d.update(flag="N")
            self.get_dict(**kwargs)
        else:
            return {}
    def get_verbose_dic(self):
        obj=self.model
        v_dic={}
        for filed in obj._meta.fields:
            v_dic[filed.name]=filed.verbose_name
        for x in ["id","project","flag"]:
            v_dic.pop(x)
        return v_dic
class GlobalDataManager(Base):
    pass

class TestCaseManager(Base):

    # def get_dicts(self,**kwargs):
    #     # 获取字典列表，包含steps[{field:vlaue},{}]
    #     testcases_dicts=super().get_dicts(**kwargs)
    #     testcases=super().all()
    #     for case in testcases_dicts:
    #         steps=testcases.get(case["id"]).casestep_set().values()
    #         case["steps"]=[s for s in steps]
    #     return  testcases_dicts

    def get_dicts(self,testcase_queryset):
        # 获取字典列表，包含steps[{field:vlaue},{}],传入testcase的queryset
        testcases_dicts=[t for t in testcase_queryset.values()]
        for case in testcases_dicts:
            steps=testcase_queryset.get(pk=case["id"]).casestep_set.all().values()
            case["steps"]=[s for s in steps]
        return  testcases_dicts

class CaseStepManager(Base):
    pass
class ElementManager(Base):
    pass
class RunCaseManager(Base):
    def get_testcases(self,**kwargs):
        r=super().get(**kwargs)
        modules = r.module.all()
        return r.plateform.testcase_set.all().filter(module_name__in=modules)
