from django.db import models

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.question_text
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
class Plateform(models.Model):
    platform_code=models.SlugField('平台编码',unique=True)
    platform_name=models.CharField('平台名称',max_length=20)
    def __str__(self):
        return self.platform_name
    class Meta:
        verbose_name = '平台信息'
        db_table = 'haptest_Plateform'
class Project(models.Model):
    project_name=models.CharField('项目名称',max_length=50,unique=True,null=False)
    platform = models.ForeignKey(Plateform,on_delete=models.CASCADE, verbose_name='所属平台', null=False,default='1')
    def __str__(self):
        return self.project_name
    class Meta:
        verbose_name = '项目信息'
        db_table = 'haptest_Project'

class Module(models.Model):
    #模块，用例集
    module_name = models.CharField('模块名称', max_length=50, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # project =models.
    def __str__(self):
        return self.module_name
    class Meta:
        verbose_name = '模块'
        db_table = 'haptest_module'

class Element(models.Model):
    plateform=models.ForeignKey(Plateform,on_delete=models.CASCADE,verbose_name='所属平台',default='1')
    page=models.CharField('页面',max_length=50)
    element=models.CharField('元素',max_length=50)
    by=models.CharField('by',max_length=50)
    custom = models.CharField('custom', max_length=50, blank=True)
    value=models.TextField('value',max_length=300)
    remark=models.TextField('备注',max_length=200,blank=True )
    def __str__(self):
        return self.element
    class Meta:
        verbose_name = '元素管理'
        db_table = 'haptest_element'
        unique_together=('page','element')
