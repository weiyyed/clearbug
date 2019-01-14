# Generated by Django 2.1.3 on 2019-01-14 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaseStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=10, verbose_name='测试步骤')),
                ('keyword', models.CharField(max_length=20, verbose_name='操作')),
                ('page', models.CharField(max_length=20, verbose_name='页面')),
                ('element', models.CharField(max_length=20, verbose_name='元素')),
                ('ele_parameter', models.CharField(blank=True, max_length=20, verbose_name='元素参数')),
                ('data', models.CharField(blank=True, max_length=20, verbose_name='测试数据')),
                ('expected', models.CharField(blank=True, max_length=20, verbose_name='预期结果')),
                ('output', models.CharField(blank=True, max_length=20, verbose_name='输出数据')),
                ('remark', models.CharField(blank=True, max_length=50, verbose_name='备注')),
            ],
            options={
                'verbose_name': '测试步骤',
                'db_table': 'haptest_casestep',
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_code', models.CharField(blank=True, max_length=30, verbose_name='组织编码')),
                ('common_code', models.CharField(blank=True, max_length=30, verbose_name='普通编码')),
                ('phone_num', models.CharField(blank=True, max_length=30, verbose_name='手机号')),
                ('flag', models.CharField(blank=True, default='N', max_length=4, verbose_name='flag')),
            ],
            options={
                'verbose_name': '测试数据',
                'db_table': 'haptest_data',
            },
        ),
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='data/import/', verbose_name='文件')),
            ],
            options={
                'verbose_name': '文件管理',
                'db_table': 'haptest_datafile',
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(max_length=50, verbose_name='页面')),
                ('element', models.CharField(max_length=50, verbose_name='元素')),
                ('by', models.CharField(max_length=50, verbose_name='by')),
                ('custom', models.CharField(blank=True, max_length=50, verbose_name='custom')),
                ('value', models.TextField(max_length=300, verbose_name='value')),
                ('remark', models.TextField(blank=True, max_length=200, verbose_name='备注')),
            ],
            options={
                'verbose_name': '元素管理',
                'db_table': 'haptest_element',
            },
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('env_name', models.CharField(max_length=20, verbose_name='环境名称')),
                ('desired_caps', models.TextField(default="{'platformName': 'Desktop', 'browserName': 'Chrome'}", verbose_name='运行参数')),
                ('pc_login_url', models.URLField(default='', max_length=50, verbose_name='登录地址')),
                ('login_user', models.CharField(max_length=10, verbose_name='用户')),
                ('login_password', models.CharField(max_length=10, verbose_name='密码')),
                ('server_url', models.URLField(blank=True, default='http://127.0.0.1:4723/wd/hub', max_length=50, verbose_name='server_url')),
            ],
        ),
        migrations.CreateModel(
            name='GlobalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varible', models.CharField(max_length=20, unique=True, verbose_name='变量名')),
                ('value', models.CharField(max_length=30, verbose_name='变量值')),
            ],
            options={
                'verbose_name': '全局变量',
                'db_table': 'haptest_global_data',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_name', models.CharField(max_length=50, verbose_name='模块名称')),
            ],
            options={
                'verbose_name': '模块',
                'db_table': 'haptest_module',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_code', models.SlugField(unique=True, verbose_name='平台编码')),
                ('platform_name', models.CharField(max_length=20, verbose_name='平台名称')),
            ],
            options={
                'verbose_name': '平台信息',
                'db_table': 'haptest_Platform',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50, unique=True, verbose_name='项目名称')),
                ('platform', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='haptest.Platform', verbose_name='所属平台')),
            ],
            options={
                'verbose_name': '项目信息',
                'db_table': 'haptest_Project',
            },
        ),
        migrations.CreateModel(
            name='RunCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runcase_name', models.CharField(max_length=20, verbose_name='构建名称')),
                ('environment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='haptest.Environment', verbose_name='运行环境')),
                ('module', models.ManyToManyField(to='haptest.Module', verbose_name='包含模块')),
                ('platform', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='haptest.Platform', verbose_name='所属平台')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='haptest.Project', verbose_name='所属项目')),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_code', models.CharField(max_length=40, unique=True, verbose_name='用例编号')),
                ('title', models.CharField(max_length=40, verbose_name='用例标题')),
                ('condition', models.CharField(blank=True, choices=[('', '---'), ('BASE', '用例集执行前执行'), ('SETUP', '每个用例执行前执行'), ('MAIN', '主用例'), ('SUB', '子用例'), ('SKIP', '跳过不执行'), ('SNIPPET', '用例片段')], max_length=40, verbose_name='前置条件')),
                ('designer', models.CharField(blank=True, max_length=20, verbose_name='设计者')),
                ('priority', models.CharField(blank=True, max_length=20, verbose_name='优先级')),
                ('remark', models.CharField(blank=True, max_length=50, verbose_name='备注')),
                ('flag', models.BooleanField(blank=True, default='True', verbose_name='自动化标记')),
                ('module_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='haptest.Module', verbose_name='所属模块')),
                ('platform', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='haptest.Platform', verbose_name='所属平台')),
            ],
            options={
                'verbose_name': '测试用例',
                'db_table': 'haptest_testcase',
            },
        ),
        migrations.AddField(
            model_name='element',
            name='platform',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='haptest.Platform', verbose_name='所属平台'),
        ),
        migrations.AddField(
            model_name='datafile',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='haptest.Project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='data',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='haptest.Project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='casestep',
            name='testcase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='haptest.TestCase', verbose_name='所属用例'),
        ),
        migrations.AlterUniqueTogether(
            name='element',
            unique_together={('page', 'element')},
        ),
    ]
