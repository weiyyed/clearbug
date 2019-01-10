from django.db import models

class Base(models.Manager):

    def get_dicts(self,**kwargs):
        # 获取字典列表，[{field:vlaue},{}]
        return  [m for m in super().filter(**kwargs).values()]
    def __get_tuples(self, field):
        # 获取元素值tuple
        ele_set = [('', "---")]
        for x in super().values('field').distinct():
            ele_set.append((x['field'],x['field']))
        return ele_set

class DataManager(Base):
    def get_data_dict(self,**kwargs):
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
                verbose_dic=self.__get_verbose_dic()
                for name,vername in verbose_dic.items():
                    new_dic[vername]=d_dicts[0][name]
                return new_dic
            else:
                d.update(flag="N")
                return self.get_data_dict(**kwargs)
        else:
            return {}
    def __get_verbose_dic(self):
        # 获取字典｛name:verbosename｝
        obj=self.model
        v_dic={}
        for filed in obj._meta.fields:
            v_dic[filed.name]=filed.verbose_name
        for x in ["id","project","flag"]:
            v_dic.pop(x)
        return v_dic
class GlobalDataManager(Base):
    def get_data_dict(self):
    #     获取全局变量字典
        data_dict={}
        g_dic_list=self.get_dicts()
        for gdic in g_dic_list:
            data_dict[gdic["varible"]]=gdic["value"]
        return data_dict

class TestCaseManager(Base):

    def get_dicts(self,testcase_queryset):
        # 获取字典列表，包含steps[{field:vlaue},{}],传入testcase的queryset
        testcases_dicts=[t for t in testcase_queryset.values()]
        for case in testcases_dicts:
            steps=testcase_queryset.get(pk=case["id"]).casestep_set.all().values()
            case["steps"]=[]
            for step in steps:
                step["element"]+=step["ele_parameter"]
                case["steps"].append(step)
            # case["steps"]=[s for s in steps]
        return  testcases_dicts
    def get_snippet_tuples(self):
        s_set=[]
        for x in self.filter(condition="SNIPPET").values("case_code"):
            s_set.append((x["case_code"],x["case_code"]))
        return s_set
class CaseStepManager(Base):
    pass
    # def get_all():
    #     obj=self.model
    #     obj.ele_parameter
    #     super().all()
class ElementManager(Base):

    def get_page_tuple(self):
        # 获取page元组
        return self.__get_tuples("page").append("用例片段", "用例片段")

    def get_element_tuples(self):
        return self.__get_tuples("element")

class RunCaseManager(Base):
    def get_testcases(self,**kwargs):
        r=super().get(**kwargs)
        modules = r.module.all()
        return r.plateform.testcase_set.all().filter(module_name__in=modules)
