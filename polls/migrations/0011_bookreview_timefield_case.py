# Generated by Django 2.1.3 on 2018-12-29 07:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20181229_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='TimeField_case',
            field=models.TimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]