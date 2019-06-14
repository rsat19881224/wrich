from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import Select
from ckeditor.widgets import CKEditorWidget

from .models import Article, ArticleDetail, Comment, Reply

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'cols': 30, 'rows': 1}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = '__all__'