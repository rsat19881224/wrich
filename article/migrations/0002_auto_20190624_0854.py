# Generated by Django 2.1.2 on 2019-06-23 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': '画像ファイル', 'verbose_name_plural': '画像ファイル'},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, '募集中'), (1, '指示中'), (2, '入稿済み'), (3, '公開済み')], default=0, verbose_name='状態'),
        ),
    ]
