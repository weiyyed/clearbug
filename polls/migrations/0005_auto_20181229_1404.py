# Generated by Django 2.1.3 on 2018-12-29 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_article_book_bookreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='review_name',
            field=models.CharField(help_text='帮助信息', max_length=30),
        ),
    ]
