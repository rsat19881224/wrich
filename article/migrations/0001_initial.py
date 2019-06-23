# Generated by Django 2.1.2 on 2019-06-20 15:14

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
                ('intro_title', models.CharField(max_length=150, verbose_name='記事名')),
                ('intro_type', models.IntegerField(choices=[(1, '【パターン1】うまくいかないのはあなたのせいではありません！'), (2, '【パターン2】これを知らないからできないんです。'), (3, '【パターン3】～だと判明！')], default=1, verbose_name='タイプ')),
                ('intro_content', models.TextField(blank=True, verbose_name='導入文')),
                ('keyword', models.TextField(blank=True, null=True, verbose_name='タグ')),
                ('check', models.BooleanField(blank=True, null=True, verbose_name='状態')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
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
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='カテゴリ名')),
                ('description', models.TextField(blank=True, verbose_name='説明')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('created_by', models.ForeignKey(blank=True, default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='CategoryCreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
            ],
            options={
                'verbose_name': 'カテゴリ',
                'verbose_name_plural': 'カテゴリ',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000, verbose_name='内容')),
                ('is_publick', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('created_by', models.ForeignKey(blank=True, default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Comment_CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Comment_Article', to='article.Article')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Comment_UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': 'コメント',
                'verbose_name_plural': 'コメント',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='タイトル')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='説明')),
                ('origin', models.ImageField(upload_to='uploads/%y/%m/%d/', verbose_name='ファイル選択')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='登録日')),
                ('created_by', models.ForeignKey(blank=True, default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='登録者')),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='お知らせ')),
                ('public_date', models.DateField(blank=True, null=True, verbose_name='公開日')),
                ('close_date', models.DateField(blank=True, null=True, verbose_name='終了日')),
                ('target_group', models.IntegerField(choices=[(1, 'ALL'), (2, 'PEEP'), (3, 'ライター')], default=1, verbose_name='対象グループ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('created_by', models.ForeignKey(blank=True, default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Info_CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Info_UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': 'お知らせ',
                'verbose_name_plural': 'お知らせ',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='オーダー名')),
                ('characters', models.IntegerField(blank=True, verbose_name='文字数（以上）')),
                ('keyword', models.TextField(blank=True, null=True, verbose_name='キーワード')),
                ('target', models.TextField(blank=True, null=True, verbose_name='ターゲット')),
                ('description', models.TextField(blank=True, verbose_name='記事内容')),
                ('note', models.TextField(blank=True, verbose_name='備考')),
                ('limit_date', models.DateField(blank=True, verbose_name='納期')),
                ('salary', models.IntegerField(blank=True, verbose_name='報酬')),
                ('order_date', models.DateField(blank=True, verbose_name='発注日')),
                ('accept_date', models.DateField(blank=True, verbose_name='受注日')),
                ('status', models.IntegerField(choices=[(0, '指示中'), (1, '執筆中'), (2, '入稿済み'), (3, '公開済み')], default=0, verbose_name='状態')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_category', to='article.Category', verbose_name='カテゴリ')),
                ('created_by', models.ForeignKey(blank=True, default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
                ('order_user', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_user', to=settings.AUTH_USER_MODEL, verbose_name='発注先')),
            ],
            options={
                'verbose_name': 'オーダー',
                'verbose_name_plural': 'オーダー',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000, verbose_name='内容')),
                ('is_public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('created_by', models.ForeignKey(blank=True, default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Reply_CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Comment')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Reply_UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': '返信',
                'verbose_name_plural': '返信',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='サイト名')),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
                ('target', models.TextField(blank=True, null=True, verbose_name='ターゲット')),
                ('description', models.TextField(blank=True, null=True, verbose_name='サイト概要')),
                ('note', models.TextField(blank=True, null=True, verbose_name='備考')),
                ('open_date', models.DateField(blank=True, null=True, verbose_name='開設日')),
                ('rank', models.IntegerField(choices=[(1, '低'), (2, '中'), (3, '高')], default=2, verbose_name='ランク')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('created_by', models.ForeignKey(blank=True, default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='site_CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
                ('orner', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='site_orner', to=settings.AUTH_USER_MODEL, verbose_name='責任者')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='site_UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': 'サイト',
                'verbose_name_plural': 'サイト',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_site', to='article.Site', verbose_name='サイト名'),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Category_Article', to='article.Category', verbose_name='カテゴリ'),
        ),
        migrations.AddField(
            model_name='article',
            name='created_by',
            field=models.ForeignKey(blank=True, default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者'),
        ),
        migrations.AddField(
            model_name='article',
            name='order_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Order_Article', to='article.Order', verbose_name='オーダー'),
        ),
        migrations.AddField(
            model_name='article',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
    ]
