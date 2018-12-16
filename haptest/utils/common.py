from sweetest.utility import Excel,data2dict
# class Parse_url():
#
#     func=None
#     @classmethod
#     def parse_url(cls,request,**kwargs):
#         #解析url
#         app=kwargs.pop('app')
#         cls.func=kwargs.pop('func')
#         id=kwargs.pop('id',None)
#         app=__import__('%s.views'%app)
#         views=getattr(app,'views')
#         views_func=getattr(views,'func')
#         return views_func(request,id) if id else views_func(request)
def file2database(excel_file,model,platform_id):
    #excel导入数据库
    excel_file_obj=Excel(excel_file)
    datas=excel_file_obj.read('import')
    datas_dic_list=data2dict(datas)
    for d in datas_dic_list:
        d['plateform_id']=platform_id
    for d_dic in datas_dic_list:
        model.objects.create(**d_dic)
