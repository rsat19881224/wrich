# Generated by Django 2.1.2 on 2019-06-05 01:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro_title', models.CharField(blank=True, max_length=150, verbose_name='記事名')),
                ('intro_type', models.IntegerField(choices=[(1, '【パターン1】うまくいかないのはあなたのせいではありません！'), (2, '【パターン2】これを知らないからできないんです。'), (3, '【パターン3】～だと判明！')], default=1, verbose_name='タイプ')),
                ('intro_content', models.TextField(blank=True, verbose_name='導入文')),
                ('keyword', models.TextField(blank=True, null=True, verbose_name='キーワード')),
                ('check', models.BooleanField(blank=True, null=True, verbose_name='入稿チェック')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='作成時間')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='更新時間')),
                ('created_by', models.ForeignKey(blank=True, default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': '記事',
                'verbose_name_plural': '記事',
            },
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='表示順')),
                ('block_title', models.CharField(max_length=150, verbose_name='見出し')),
                ('block_content', models.TextField(verbose_name='内容')),
                ('Article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
    ]
