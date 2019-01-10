import os
from sweetest.utility import Excel,data2dict

def upload2database(file_obj,model,platform=None):
    # 处理上传文件存数据库
    upload_file = os.path.join('upload', file_obj.name)
    with open(upload_file, 'wb') as data:
        for line in file_obj.chunks():
            data.write(line)
    file2database(upload_file, model, platform_id=platform)
    os.remove(upload_file)


def file2database(excel_file,model,platform_id=None):
    #excel转数据库
    excel_file_obj=Excel(excel_file)
    datas=excel_file_obj.read('import')
    if not datas:
        print("excel文件读取为空")
    datas_dic_list=data2dict(datas)
    if platform_id:
        for d in datas_dic_list:
            d['plateform_id']=platform_id
    for d_dic in datas_dic_list:
        model.objects.update_or_create(**d_dic)
