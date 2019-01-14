import os,copy
from sweetest.utility import Excel,data2dict
from sweetest.config import all_keywords
from haptest.models import TestCase, CaseStep
from django.db.models import Model


def upload2dicts(file_obj,platform_id=None,module_name_id=None):
    # 处理上传文件存数据库,字典参数为id
    upload_file = os.path.join('upload', file_obj.name)
    with open(upload_file, 'wb') as data:
        for line in file_obj.chunks():
            data.write(line)
    # file2database(upload_file, model, platform_id=platform)
    # excel转数据库
    excel_file_obj = Excel(upload_file)
    os.remove(upload_file)
    datas = excel_file_obj.read('import')
    if not datas:
        print("excel文件读取为空")
    datas_dic_list = data2dict(datas)
    for k in ["platform_id", "module_name_id"]:
        if eval(k):
            for d in datas_dic_list:
                d[k] = eval(k)
    #   用例集转换
    return datas_dic_list


def testcases2standard(testcase_dics):
#     用例字典转换为用例主子：[{testcase:{..},steps{[...]}},{....}]
    testsuite = [] #返回值
    testcase_step_dic = {} #用例步骤字典
    testcase_dic_std ={} #标准用例字典
    step_dic={} #步骤字典
    step_dic_list=[]
    case_field_list=[] #用例遍历的字段
    step_field_list=[] #步骤遍历的字段
    for testcase_dic in testcase_dics:

        # for key,value in testcase_dic:
        if testcase_dic["id"]:
            if testcase_step_dic:
                testsuite.append(copy.deepcopy(testcase_step_dic))
            # testcase_step_dic["testcase"] = testcase_dic_std
            # testsuite.append(testcase_step_dic)
                testcase_step_dic.clear()
            if not case_field_list:
                case_field_list=[f.name for f in TestCase._meta.get_fields()]
                case_field_list.extend(["platform_id","module_name_id"])
                for f in ["casestep","id","case_code","platform", "module_name",]:
                    case_field_list.remove(f)
            for x in case_field_list:
                testcase_dic_std[x]=testcase_dic[x]
            testcase_dic_std["case_code"]=testcase_dic["id"]
            if testcase_dic_std["flag"].lower() in ("true",""):
                testcase_dic_std["flag"]="True"
            else:
                testcase_dic_std["flag"] = "False"

            testcase_step_dic["testcase"] = testcase_dic_std
        if not step_field_list:
            step_field_list=[f.name for f in CaseStep._meta.get_fields()]
            step_field_list.remove("testcase")
            step_field_list.remove("id")
            step_field_list.remove("no")

        for s in step_field_list:
            # 替换kewword为编码
            if s=="keyword":
                step_dic[s] = all_keywords.get(testcase_dic[s])
            else:
                step_dic[s]=testcase_dic[s]
        step_dic["no"]=testcase_dic["step"]
        step_dic_list.append(step_dic.copy())
        testcase_step_dic["steps"] = step_dic_list
    return testsuite

def dic2database(datas_dic_list,Model):
    # 单表保存
    for d_dic in datas_dic_list:
        Model.objects.update_or_create(**d_dic)

def testcase2database(datas_dic_list):
    # 用例主子表保存
    case_dics=testcases2standard(datas_dic_list)
    for case_dic in case_dics:
        case_obj=TestCase.objects.update_or_create(case_code=case_dic["testcase"]["case_code"],defaults=case_dic["testcase"])[0]
        for step in case_dic["steps"]:
            case_obj.casestep_set.update_or_create(**step)




