from django.contrib import admin
from haptest.models import Project,Platform,TestCase,CaseStep,Element,Data,Module,Environment,RunCase
from sweetest.runcase import Autotest4database
from django.utils.text import capfirst
from django.utils.datastructures import OrderedDict

# 排序设置，按注册顺序排序
def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count

def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse
    return inner

admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)

# 注册
admin.site.register(Platform)
admin.site.register(Project)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("page", "element", "by","platform","value", )
    list_filter = ("platform", "page")
    # list_per_page = 10
    list_display_links = ("page", "element",)
    search_fields = ("page", "element","value", "platform")
admin.site.register(Element,ElementAdmin)
admin.site.register(Data)
admin.site.register(Module)
admin.site.register(Environment)


class CasestepInline(admin.TabularInline):
    model = CaseStep
    extra = 0
class TestCaseAdmin(admin.ModelAdmin):
    # fieldsets = {
    #     (None:{"fields":["case_code","case_title"]})
    # }
    list_display = ("case_code","title","platform","condition","module_name","run_order","designer")
    list_display_links = ("case_code","title",)
    list_filter = ("platform","module_name")
    list_per_page = 10
    search_fields = ("case_code","title",)
    inlines = [CasestepInline]
admin.site.register(TestCase,TestCaseAdmin)

import threading
class RunCaseAdmin(admin.ModelAdmin):
    list_display = ("runcase_name", "project", "environment", "platform",)
    # list_filter = ("platform", "page")
    # list_per_page = 10
    # list_display_links = ("runcase_name",)
    # search_fields = ("runcase_name", "project", "environment", "platform",)

    # 定义运行动作
    actions = ["run",]
    def run(self, request, queryset):
        if len(queryset)>1:
            self.message_user(request,"只能选择一条数据执行")
        else:
            run_case_obj = queryset[0]
            # 只同时运行一个用例
            for t in threading.enumerate():
                if "runcase" in t.getName():
                    self.message_user(request, "有其他用例在执行中，请等待")
                    return
            t=threading.Thread(target=Autotest4database(run_case_obj=queryset[0]).plan,name='runcase')
            t.start()
            self.message_user(request,"用例开始运行")
    run.short_description = '运行'
admin.site.register(RunCase,RunCaseAdmin)