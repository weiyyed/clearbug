from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Project(models.Model):
    project_name=models.CharField('项目名称',max_length=50,unique=True,null=False)
    def __str__(self):
        return self.project_name
    # class Meta:
    #     verbose_name = '项目信息'
    #     db_table = 'Project'

class Module(models.Model):
    #模块，用例集

    module_name = models.CharField('模块名称', max_length=50, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Element(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    page=models.CharField(max_length=50, null=False)
    element=models.CharField(max_length=50, null=False)
    by=models.CharField(max_length=50, null=False)
    value=models.CharField(max_length=50, null=False)
    custom=models.CharField(max_length=50, null=False)
    remark=models.CharField(max_length=50, null=False)
