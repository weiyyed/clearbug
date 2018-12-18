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

class Date(models.Model):
    #数据
    project=models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='所属项目')
    org_code=models.CharField('组织编码',max_length=30,blank=True)
    common_code=models.CharField('普通编码',max_length=30,blank=True)
    phone_num=models.CharField('人员手机号',max_length=30,blank=True)
    flag=models.CharField('flag',max_length=4,blank=True)

class DateFile(models.Model):
    #数据
    project=models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='所属项目')
    file=models.FileField('文件',upload_to='data/import/')
class TestCase(models.Model):
    #用例
    project=models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='所属项目')
    case_code=models.CharField('用例编号',max_length=40,)
    title=models.CharField('用例标题',max_length=40,)
    condition=models.CharField('前置条件',max_length=40,)
    designer=models.CharField('设计者',max_length=20,)
    priority=models.CharField('优先级',max_length=20,)
    remark=models.CharField('备注',max_length=50,)

class CaseStep(models.Model):
    #步骤
    no = models.CharField('测试步骤', max_length=10, )
    keyword = models.CharField('操作', max_length=10, )
    page = models.CharField('页面', max_length=10, )
    element = models.CharField('元素', max_length=10, )
    data = models.CharField('测试数据', max_length=10, )
    expected = models.CharField('预期结果', max_length=10, blank=True)
    output = models.CharField('输出数据', max_length=10, )
    remark = models.CharField('备注', max_length=50, )