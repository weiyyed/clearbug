from django.db import models

class Base(models.Manager):

    def to_testcase_dicts(self, **kwargs):
        # 获取字典列表，[{field:vlaue},{}]
        return  [m for m in super().filter(**kwargs).values()]
    def _get_tuples(self, field):
        # 获取元素值tuple
        ele_set = [('', "---")]
        for x in super().values(field).distinct():
            ele_set.append((x[field],x[field]))
        return ele_set

class DataManager(Base):
    def get_data_dict(self,**kwargs):
        dataset=super().filter(**kwargs)
        if not dataset:
            return {}
        data_dict={}
        for data in dataset:
            data_dict[data.name] = data.value
            if data.current_seq_num:
                next_num=self._increase(data.current_seq_num)
                filter(name=data).update(current_seq_num=next_num)
                super().filter(name=data).update(current_seq_num=next_num)
        return data_dict
    def _increase(self,num_str):
        while True:
            lenth=len(num_str)
            yield str(int(num_str)+1).zfill(lenth)



        # # 获取第一条未使用数据
        # d=super().filter(**kwargs)
        # if d:
        #     data_first=d.exclude(flag="Y")[:1]
        #     d_dicts=data_first.values()[:1]
        #     new_dic = {}
        #     if d_dicts:
        #         # 重置为N
        #         d_dicts=[d for d in d_dicts]
        #         super().filter(pk=data_first.get().id).update(flag="Y")
        #         verbose_dic=self.__get_verbose_dic()
        #         for name,vername in verbose_dic.items():
        #             new_dic[vername]=d_dicts[0][name]
        #         return new_dic
        #     else:
        #         d.update(flag="N")
        #         return self.get_data_dict(**kwargs)
        # else:
        #     return {}
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
        g_dic_list=self.to_testcase_dicts()
        for gdic in g_dic_list:
            data_dict[gdic["varible"]]=gdic["value"]
        return data_dict

class TestCaseManager(Base):

    def to_testcase_dicts(self, testcase_queryset):
        # 获取字典格式的用例，包含steps[{field:vlaue},{}],传入testcase的queryset，连接元素和元素参数
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
    def get_snippet_code_dics(self):
#         获取｛用例片段：[casecode,]｝的字典
        return {"用例片段":[c[0] for c in super().filter(condition="SNIPPET").values_list("case_code")]}
class CaseStepManager(Base):
    pass
    # def get_all():
    #     obj=self.model
    #     obj.ele_parameter
    #     super().all()
class ElementManager(Base):

    def get_page_tuples(self):
        # 获取page元组并添加用例片段选项
        p_list=self._get_tuples("page")
        p_list.append(("用例片段", "用例片段"))
        return p_list

    def get_element_tuples(self):
        # 获取element元组
        return self._get_tuples("element")
    def get_page_ele_dic(self):
        # 获取页面-元组的字典
        e_obj = super().all()
        ele = []
        page_ele_dic = {}
        for e in e_obj:
            if page_ele_dic.get(e.page, None):
                page_ele_dic[e.page].append(e.element)
            else:
                page_ele_dic[e.page] = [e.element]
        return page_ele_dic
class RunCaseManager(Base):
    def get_testcases(self,**kwargs):
        r=super().get(**kwargs)
        modules = r.module.all()
        return r.platform.testcase_set.all().filter(module_name__in=modules)

