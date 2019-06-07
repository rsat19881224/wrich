from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from pure_pagination.mixins import PaginationMixin

from .filters import ArticleFilterSet
from .forms import ArticleForm, ArticleDetailFormSet
from .models import Article


class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ArticleMixin(object):
    def form_valid(self, form, formset):

        # formset.saveでインスタンスを取得できるように、既存データに変更が無くても更新対象となるようにする
        for detail_form in formset.forms:
            if detail_form.cleaned_data:
                detail_form.has_changed = lambda: True

        # インスタンスの取得
        article = form.save(commit=False)
        formset.instance = article
        details = formset.save(commit=False)

        sub_total = 0

#        # 明細に単価と合計を設定
#        for detail in details:
#            detail.unit_price = detail.item.unit_price
#            detail.amount = detail.unit_price * detail.quantity
#            sub_total += detail.amount
#
#        # 見出しに小計、消費税、合計、担当者を設定
#        tax = round(sub_total * 0.08)
#        total_amount = sub_total + tax
#
#        article.sub_total = sub_total
#        article.tax = tax
#        article.total_amount = total_amount
        article.created_by = self.request.user

        # DB更新
        with transaction.atomic():
            article.save()
            formset.instance = article
            formset.save()

        # 処理後は詳細ページを表示
        return redirect(article.get_absolute_url())

class ArticleFilterView(LoginRequiredMixin, PaginationMixin, FilterView):
    model = Article
    filterset_class = ArticleFilterSet

    queryset = Article.objects.all().order_by('-created_at')

    # 1ページの表示
    paginate_by = 20
    object = Article

    def get(self, request, **kwargs):
        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)


class ArticleDetailView(LoginRequiredMixin, DetailView):

    model = Article


class ArticleCreateView(LoginRequiredMixin, ArticleMixin, FormsetMixin, CreateView):
    template_name = 'article/article_form.html'
    model = Article
    form_class = ArticleForm
    formset_class = ArticleDetailFormSet


class ArticleUpdateView(LoginRequiredMixin, ArticleMixin, FormsetMixin, UpdateView):
    is_update_view = True
    template_name = 'article/article_form.html'
    model = Article
    form_class = ArticleForm
    formset_class = ArticleDetailFormSet


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('index')
