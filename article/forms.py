from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import Select
from ckeditor.widgets import CKEditorWidget
import bootstrap_datepicker_plus as datetimepicker
from logging import getLogger
logger = getLogger(__name__)
from .models import Article, ArticleDetail, ArticleFix, Comment, Reply, Category, Site, Order, Info, Image

INTRO_WRITE_TYPE = (
        (1, '【パターン1】うまくいかないのはあなたのせいではありません！'), 
        (2, '【パターン2】これを知らないからできないんです。'), 
        (3, '【パターン3】～だと判明！'))

#独自ラジオボタンウィジェット作成
class BS4RadioSelect(forms.RadioSelect):
    input_type = 'radio'
    template_name = 'widgets/bs4_radio.html'

#独自チェックボックスウィジェット作成
class BS4CheckboxInline(forms.CheckboxSelectMultiple):
    input_type = 'checkbox'
    template_name = 'widgets/bs4_checkbox_inline.html'

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    #各フィールドに対するバリデーションチェック↓ clean_xxxx
    #is_validを抜けてきたデータをごにょごにょする
    def clean_intro_title(self):
        intro_title = self.cleaned_data.get('intro_title')
        if intro_title in ('ばか', 'あほ', 'まぬけ', 'うんこ'):
            self.add_error('intro_title', '　※名前に暴言を含めないでください。')
            if intro_title == 'ばか':
                self.add_error('intro_title', 'ばかは特にダメです。')
        return intro_title

    intro_type = forms.ChoiceField(
        label='導入タイプ',
        widget=BS4RadioSelect,
        choices=INTRO_WRITE_TYPE,
        initial=1,
    )

class ArticleDetailForm(forms.ModelForm):
    class Meta:
        model = ArticleDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArticleDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            logger.debug(field)
            field.widget.attrs["class"] = "form-control"

        #self.fields['item'].choices = lambda: [('', '-- 商品 --')] + [
        #    (item.id, '%s %s円' % (item.name.ljust(10, '　'), item.unit_price)) for item in
        #    Item.objects.order_by('order')]

        #choices_number = [('', '-- 個数 --')] + [(str(i), str(i)) for i in range(1, 10)]
        #self.fields['quantity'].widget = Select(choices=choices_number)

ArticleDetailFormSet = inlineformset_factory(
    parent_model=Article,
    model=ArticleDetail,
    form=ArticleDetailForm,
    extra=0,
    min_num=1,
    validate_min=True,
)

class ArticleFixForm(forms.ModelForm):
    class Meta:
        model = ArticleFix
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArticleFixForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
        widgets = {
            'open_date': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'limit_date': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ),
            'order_date': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ).start_of('期間'),

            'accept_date': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ).end_of('期間'),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = '__all__'
        widgets = {
            'public_date': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ).start_of('期間'),

            'close_date': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ).end_of('期間'),
        }
    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class ImageForm(forms.ModelForm):
    origin = forms.ImageField(
            label='画像ファイル',
            widget=forms.ClearableFileInput(attrs={'multiple': True})
        )
    class Meta:
        model = Image
        fields = ["title","description", "origin"]
        
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
