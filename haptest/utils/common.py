import os
from sweetest.utility import Excel,data2dict
from haptest.models import TestCase, CaseStep


def upload2dicts(file_obj,model,platform_id=None,module_id=None):
    # 处理上传文件存数据库
    upload_file = os.path.join('upload', file_obj.name)
    with open(upload_file, 'wb') as data:
        for line in file_obj.chunks():
            data.write(line)
    os.remove(upload_file)
    # file2database(upload_file, model, platform_id=platform)
    # excel转数据库
    excel_file_obj = Excel(upload_file)
    datas = excel_file_obj.read('import')
    if not datas:
        print("excel文件读取为空")
    datas_dic_list = data2dict(datas)
    for k in ["platform_id", "module_id"]:
        if eval(k):
            for d in datas_dic_list:
                d[k] = eval(k)
    #   用例集转换
    return datas_dic_list


def testcases2standard(testcase_dics):
#     用例字典转换为用例主子：[{testcase:{..},steps{[...]}},{....}]
    testsuite = []
    testcase_step_dic = {}
    testcase_dic_std ={}
    step_dic={}
    step_dic_list=[]
    for testcase_dic in testcase_dics:

        for key,value in testcase_dic:
            if testcase_dic["id"]:
                testcase_step_dic["testcase"] = testcase_dic_std
                testsuite.append(testcase_step_dic)
                testcase_step_dic.clear()
                for x in [f.name for f in TestCase._meta.get_fields()].pop("casestep","id"):
                    testcase_dic_std[x]=testcase_dic[x]
            for s in [[f.name for f in CaseStep._meta.get_fields()]].pop("testcase","id"):
                step_dic[s]=testcase_dic[s]
            step_dic["no"]=step_dic.pop("step")
            testcase_step_dic["steps"] = step_dic_list.append(step_dic)
    return testsuite

def dic2database(datas_dic_list):
    # 单表保存
    for d_dic in datas_dic_list:
        model.objects.update_or_create(**d_dic)

def testcase2database(datas_dic_list):
    # 用例主子表保存
    case_dics=testcases2standard(datas_dic_list)
    for case_dic in case_dics:
        case_obj=TestCase.objects.update_or_create(case_dic["testcase"])
        for step in case_dic["steps"]:
            case_obj.casestep_set.update_or_create(step)




