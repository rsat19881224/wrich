from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import Select

from .models import Article, ArticleDetail


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


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