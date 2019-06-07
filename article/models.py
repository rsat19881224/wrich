from django.db import models
from django.core import validators
from users.models import User
from django.urls import reverse

class Article(models.Model):
    INTRO_WRITE_TYPE = (
        (1, '【パターン1】うまくいかないのはあなたのせいではありません！'), 
        (2, '【パターン2】これを知らないからできないんです。'), 
        (3, '【パターン3】～だと判明！'))
    intro_title = models.CharField(verbose_name='記事名', max_length=150, blank=True,)
    intro_type = models.IntegerField(verbose_name='タイプ', choices=INTRO_WRITE_TYPE, default=1,)
    intro_content = models.TextField(verbose_name='導入文', blank=True,)
    keyword = models.TextField(verbose_name='キーワード', blank=True, null=True,)
    check = models.BooleanField(verbose_name='状態',blank=True, null=True,)

    # 以下、管理項目
    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
        default=1,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.intro_title

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '記事'
        verbose_name_plural = '記事'

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

#20190604 追加
class ArticleDetail(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE)

    order_id = models.IntegerField(verbose_name='表示順', blank=True, null=True,validators=[validators.MinValueValidator(0)],)
    block_title = models.CharField(verbose_name='見出し', max_length=150,)
    block_content = models.TextField(verbose_name='内容',)
