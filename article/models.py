from django.db import models
from django.core import validators
from users.models import User
from django.urls import reverse
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

#20190620
class Image(models.Model):
    title = models.CharField(verbose_name='タイトル', blank=True, null=True,max_length=255)
    description = models.CharField(verbose_name='説明',max_length=255, blank=True, null=True,)
    origin = models.ImageField(verbose_name='ファイル選択',upload_to="uploads/%y/%m/%d/")
    big = ImageSpecField(source="origin",processors=[ResizeToFill(1280, 1024)],format='JPEG')
    thumbnail = ImageSpecField(source='origin',processors=[ResizeToFill(250,250)],format="JPEG",options={'quality': 60})
    middle = ImageSpecField(source='origin',processors=[ResizeToFill(600, 400)],format="JPEG",options={'quality': 75})
    small = ImageSpecField(source='origin',processors=[ResizeToFill(75,75)],format="JPEG",options={'quality': 50})
    created_by = models.ForeignKey(
        User,
        verbose_name='登録者',
        blank=True,
        null=True,
        related_name='image_CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
        default=1,
    )
    created_at = models.DateTimeField(verbose_name='登録日',auto_now=True)

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '画像ファイル'
        verbose_name_plural = '画像ファイル'

#20190617
class Site(models.Model):
    SITE_TYPE = (
        (1, '低'), 
        (2, '中'), 
        (3, '高'))
    title = models.CharField(verbose_name='サイト名', max_length=150, blank=False,)
    url = models.CharField(verbose_name='URL', max_length=255, blank=False,)
    target = models.TextField(verbose_name='ターゲット', blank=True, null=True,)
    description = models.TextField(verbose_name='サイト概要', null=True, blank=True,)
    note = models.TextField(verbose_name='備考', null=True, blank=True,)
    open_date = models.DateField(verbose_name='開設日',null=True, blank=True,)
    rank = models.IntegerField(verbose_name='ランク', choices=SITE_TYPE, default=2,)
    orner = models.ForeignKey(User,verbose_name='責任者',related_name='site_orner',on_delete=models.SET_NULL,blank=True, null=True,default=1)
    
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='site_CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
        default=1,
    )
    created_at = models.DateTimeField(verbose_name='作成日',auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='site_UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )
    updated_at = models.DateTimeField(verbose_name='更新日',auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'サイト'
        verbose_name_plural = 'サイト'

    def get_absolute_url(self):
        return reverse('site_detail', args=[str(self.id)])

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
    created_at = models.DateTimeField(verbose_name='作成日',auto_now_add=True)

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

#20190617
class Order(models.Model):
    STATUS_TYPE = (
        (0, '募集中'), 
        (1, '指示中'), 
        (2, '入稿済み'), 
        (3, '公開済み'))
    site = models.ForeignKey(Site,verbose_name='サイト名',related_name='order_site',on_delete=models.CASCADE)
    title = models.CharField(verbose_name='オーダー名', max_length=150, blank=False,)
    characters = models.IntegerField(verbose_name='文字数（以上）', blank=True,)
    keyword = models.TextField(verbose_name='キーワード', blank=True, null=True,)
    target = models.TextField(verbose_name='ターゲット', blank=True, null=True,)
    description = models.TextField(verbose_name='記事内容', blank=True,)
    note = models.TextField(verbose_name='備考', blank=True,)
    limit_date = models.DateField(verbose_name='納期',blank=True,)
    salary = models.IntegerField(verbose_name='報酬', blank=True,)
    order_user = models.ForeignKey(User,verbose_name='発注先',related_name='order_user',on_delete=models.SET_NULL, blank=True, null=True,default=1)
    order_date = models.DateField(verbose_name='発注日',blank=True,)
    accept_date = models.DateField(verbose_name='受注日',blank=True,)
    category = models.ForeignKey(Category,verbose_name='カテゴリ',related_name='order_category',null=True, blank=True,on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='状態', choices=STATUS_TYPE, default=0,)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='order_CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
        default=1,
    )
    created_at = models.DateTimeField(verbose_name='作成日',auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='order_UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )
    updated_at = models.DateTimeField(verbose_name='更新日',auto_now=True)

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.title

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'オーダー'
        verbose_name_plural = 'オーダー'

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])

class Article(models.Model):
    INTRO_WRITE_TYPE = (
        (1, '【パターン1】うまくいかないのはあなたのせいではありません！'), 
        (2, '【パターン2】これを知らないからできないんです。'), 
        (3, '【パターン3】～だと判明！'))
    intro_title = models.CharField(verbose_name='記事名', max_length=150, blank=False,)
    intro_type = models.IntegerField(verbose_name='タイプ', choices=INTRO_WRITE_TYPE, default=1,)
    intro_content = models.TextField(verbose_name='導入文', blank=True,)
    category = models.ForeignKey(Category,verbose_name='カテゴリ',related_name='Category_Article',null=True, blank=True,on_delete=models.CASCADE)
    keyword = models.TextField(verbose_name='タグ', blank=True, null=True,)
    check = models.BooleanField(verbose_name='状態',blank=True, null=True,)
    order_id = models.ForeignKey(Order,verbose_name='オーダー',related_name='Order_Article', null=True, blank=True,on_delete=models.CASCADE,db_constraint=False)
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
    created_at = models.DateTimeField(verbose_name='作成日',auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )
    updated_at = models.DateTimeField(verbose_name='更新日',auto_now=True)

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

class ArticleFix(models.Model):
    articledetail = models.ForeignKey(
        ArticleDetail,
        on_delete=models.CASCADE)
    block_fix = models.TextField(verbose_name='指摘',blank=True, null=True,)
    confirm_date = models.DateField(verbose_name='確認日',blank=True, null=True,)
    close_date = models.DateField(verbose_name='対応日',blank=True, null=True,)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='Fix_CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
        default=1,
    )
    created_at = models.DateTimeField(verbose_name='作成日',auto_now_add=True)

    def __str__(self):
        return self.block_fix

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '指摘'
        verbose_name_plural = '指摘'

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
    created_at = models.DateTimeField(verbose_name='作成日',auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='Comment_UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )
    updated_at = models.DateTimeField(verbose_name='更新日',auto_now=True)

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
    created_at = models.DateTimeField(verbose_name='作成日',auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='Reply_UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )
    updated_at = models.DateTimeField(verbose_name='更新日',auto_now=True)

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


#20190619 お知らせ機能
class Info(models.Model):
    TARGET_TYPE = (
        (1, 'ALL'), 
        (2, 'PEEP'), 
        (3, 'ライター'))
    note = models.TextField(verbose_name='お知らせ', blank=False,)
    public_date = models.DateField(verbose_name='公開日',null=True, blank=True,)
    close_date = models.DateField(verbose_name='終了日',null=True, blank=True,)
    target_group = models.IntegerField(verbose_name='対象グループ', choices=TARGET_TYPE, default=1)
    
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='Info_CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
        default=1,
    )
    created_at = models.DateTimeField(verbose_name='作成日',auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='Info_UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )
    updated_at = models.DateTimeField(verbose_name='更新日',auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'お知らせ'
        verbose_name_plural = 'お知らせ'

    def get_absolute_url(self):
        return reverse('info_detail', args=[str(self.id)])