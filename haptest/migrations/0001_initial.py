# Generated by Django 2.1.3 on 2018-12-06 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(max_length=50)),
                ('element', models.CharField(max_length=50)),
                ('by', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('custom', models.CharField(max_length=50)),
                ('remark', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_name', models.CharField(max_length=50, verbose_name='模块名称')),
            ],
        ),
        migrations.CreateModel(
            name='Plateform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_code', models.SlugField(unique=True, verbose_name='平台编码')),
                ('platform_name', models.CharField(max_length=20, verbose_name='平台名称')),
            ],
            options={
                'verbose_name': '平台信息',
                'db_table': 'haptest_Plateform',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50, unique=True, verbose_name='项目名称')),
                ('platform', models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='haptest.Plateform')),
            ],
            options={
                'verbose_name': '项目信息',
                'db_table': 'haptest_Project',
            },
        ),
        migrations.AddField(
            model_name='module',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='haptest.Project'),
        ),
        migrations.AddField(
            model_name='element',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='haptest.Project'),
        ),
    ]
