# Generated by Django 2.1.2 on 2019-06-26 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20190624_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articledetail',
            name='block_fix',
        ),
        migrations.AddField(
            model_name='order',
            name='pay_date',
            field=models.DateField(blank=True, null=True, verbose_name='支払日'),
        ),
    ]
