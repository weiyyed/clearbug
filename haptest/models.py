from django.db import models

from haptest.managers import TestCaseManager, CaseStepManager, ElementManager
from sweetest.config import web_keywords,common_keywords

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
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
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

    objects=ElementManager()

class Date(models.Model):
    #数据
    project=models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='所属项目')
    org_code=models.CharField('组织编码',max_length=30,blank=True)
    common_code=models.CharField('普通编码',max_length=30,blank=True)
    phone_num=models.CharField('人员手机号',max_length=30,blank=True)
    flag=models.CharField('flag',max_length=4,blank=True)
    def __str__(self):
        return self.project,self.org_code,self.common_code
    class Meta:
        verbose_name = '测试数据'
        db_table = 'haptest_date'

class DateFile(models.Model):
    #数据
    project=models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='所属项目')
    file=models.FileField('文件',upload_to='data/import/')
    def __str__(self):
        return self.file
    class Meta:
        verbose_name = '文件管理'
        db_table = 'haptest_datafile'
class TestCase(models.Model):
    #用例
    objects=TestCaseManager()
    condition_choices=[("","---"),
                       ("BASE","用例集执行前执行"),
                       ("SETUP","每个用例执行前执行"),
                       ("MAIN","主用例"),
                       ("SUB","子用例"),
                       ("SKIP","跳过不执行"),
                       ("SNIPPET","用例片段"),
                       ]
    plateform = models.ForeignKey(Plateform, on_delete=models.SET_NULL, verbose_name='所属平台', null=True)
    project=models.ForeignKey(Project,on_delete=models.SET_NULL,verbose_name='所属项目',blank=True,null=True)
    module_name=models.ForeignKey(Module,verbose_name='所属模块',on_delete=models.SET_NULL,null=True,blank=False)
    case_code=models.CharField('用例编号',max_length=40,)
    title=models.CharField('用例标题',max_length=40,)
    condition=models.CharField('前置条件',max_length=40,blank=True,choices=condition_choices)
    designer=models.CharField('设计者',max_length=20,blank=True)
    priority=models.CharField('优先级',max_length=20,blank=True)
    remark=models.CharField('备注',max_length=50,blank=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '测试用例'
        db_table = 'haptest_testcase'

class CaseStep(models.Model):
    #步骤
    objects=CaseStepManager()
    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='所属用例')
    no = models.CharField('测试步骤', max_length=10, )
    # choices=[]
    keyword = models.CharField('操作', max_length=20)
    page = models.CharField('页面', max_length=20, )
    element = models.CharField('元素', max_length=20, )
    data = models.CharField('测试数据', max_length=20,blank=True )
    expected = models.CharField('预期结果', max_length=20, blank=True)
    output = models.CharField('输出数据', max_length=20, blank=True)
    remark = models.CharField('备注', max_length=50,blank=True )
    def __str__(self):
        return self.no,self.keyword,self.page,self.element
    class Meta:
        verbose_name = '测试步骤'
        db_table = 'haptest_casestep'
class Environment(models.Model):
    # 环境
    env_name=models.CharField('环境名称',max_length=20)
    desired_caps=models.TextField('运行参数',default="{'platformName': 'Desktop', 'browserName': 'Chrome'}")
    pc_url=models.CharField('pc端地址',default='',max_length=50)
    server_url=models.CharField('server_url',default='',max_length=50,blank=True)
    def __str__(self):
        return self.env_name
class RunCase(models.Model):
    # 运行用例
    runcase_name=models.CharField("构建名称",max_length=20)
    plateform = models.ForeignKey(Plateform, on_delete=models.SET_NULL, verbose_name='所属平台', null=True)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    module=models.ManyToManyField(Module,verbose_name="包含模块")
    environment=models.ForeignKey(Environment,on_delete=models.SET_NULL,null=True,verbose_name="运行环境")
    def __str__(self):
        return self.runcase_name