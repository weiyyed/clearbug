# Generated by Django 2.1.3 on 2018-12-29 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_bookreview_timefield_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='ForeignKey_case',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.BookReview'),
            preserve_default=False,
        ),
    ]