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
    inlines = [CasestepInline]
admin.site.register(TestCase,TestCaseAdmin)