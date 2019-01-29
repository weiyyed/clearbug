from django.contrib import admin
from haptest.models import Project,Platform,TestCase,CaseStep
admin.site.register(Project)
admin.site.register(Platform)

class CasestepInline(admin.TabularInline):
    model = CaseStep
    extra = 0
class TestCaseAdmin(admin.ModelAdmin):
    # fieldsets = {
    #     (None:{"fields":["case_code","case_title"]})
    # }
    list_display = ("case_code","title","platform","module_name","designer")
    list_display_links = ("case_code","title",)
    list_filter = ("platform","module_name")
    list_per_page = 10
    search_fields = ("case_code","title",)
    inlines = [CasestepInline]
admin.site.register(TestCase,TestCaseAdmin)