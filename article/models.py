from django.db import models
from django.core import validators
from users.models import User
from django.urls import reverse

#20190615
class Category(models.Model):
    name = models.CharField(verbose_name='カテゴリ名', max_length=100, null=True,)
    description = models.TextField(verbose_name='説明', blank=True,)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CategoryCreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
        default=1,
    )
    created_at = models.DateTimeField(verbose_name='作成時間',auto_now_add=True)

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.name

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])

class Article(models.Model):
    INTRO_WRITE_TYPE = (
        (1, '【パターン1】うまくいかないのはあなたのせいではありません！'), 
        (2, '【パターン2】これを知らないからできないんです。'), 
        (3, '【パターン3】～だと判明！'))
    intro_title = models.CharField(verbose_name='記事名', max_length=150, blank=False,)
    intro_type = models.IntegerField(verbose_name='タイプ', choices=INTRO_WRITE_TYPE, default=1,)
    intro_content = models.TextField(verbose_name='導入文', blank=True,)
    category = models.ForeignKey(Category,verbose_name='カテゴリ',related_name='Category_Article',on_delete=models.CASCADE)
    keyword = models.TextField(verbose_name='タグ', blank=True, null=True,)
    check = models.BooleanField(verbose_name='状態',blank=True, null=True,)
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
    created_at = models.DateTimeField(verbose_name='作成時間',auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )
    updated_at = models.DateTimeField(verbose_name='更新時間',auto_now=True)

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

#20190604
class ArticleDetail(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE)

    order_id = models.IntegerField(verbose_name='表示順', blank=True, null=True,validators=[validators.MinValueValidator(0)],)
    block_title = models.CharField(verbose_name='見出し', max_length=150,)
    block_content = models.TextField(verbose_name='内容',)

#20190612 記事に対してコメント紐付け
class Comment(models.Model):
    target = models.ForeignKey(Article,related_name='Comment_Article',on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容',max_length=1000,)
    is_publick = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='Comment_CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
        default=1,
    )
    created_at = models.DateTimeField(verbose_name='作成時間',auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='Comment_UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )
    updated_at = models.DateTimeField(verbose_name='更新時間',auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント'

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

#20190612 コメントに対しての返信
class Reply(models.Model):
    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容',max_length=1000,)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='Reply_CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
        default=1,
    )
    created_at = models.DateTimeField(verbose_name='作成時間',auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='Reply_UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )
    updated_at = models.DateTimeField(verbose_name='更新時間',auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '返信'
        verbose_name_plural = '返信'

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])