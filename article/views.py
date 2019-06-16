from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from logging import getLogger
logger = getLogger(__name__)

from .filters import ArticleFilterSet, CategoryFilterSet
from .forms import ArticleForm, ArticleDetailFormSet, CommentForm, ReplyForm, CategoryForm
from .models import Article, ArticleDetail, Comment, Reply, Category

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
            logger.debug(formset)
            logger.debug(formset.errors)
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
        
        #updateの時
        if getattr(self, 'is_update_view', False):
            article.updated_by = self.request.user
        else:
            article.created_by = self.request.user

        # DB更新
        with transaction.atomic():
            article.save()
            messages.info(self.request, f'記事を作成しました。 タイトル:{article.intro_title} pk:{article.pk}')
            formset.instance = article
            formset.save()

        # 処理後は詳細ページを表示
        return redirect(article.get_absolute_url())

class ArticleFilterView(LoginRequiredMixin, PaginationMixin, FilterView):
    model = Article
    filterset_class = ArticleFilterSet

    queryset = Article.objects.all().order_by('-created_at')

    # 1ページの表示
    paginate_by = 10
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

    def get_context_data(self, **kwargs):
        article_pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)

        context['comment_list'] = Comment.objects.filter(target=article_pk)
        
        # htmlプレビュー用データ作成
        obj = Article.objects.get(id=article_pk)
        objdetail = ArticleDetail.objects.select_related().filter(
            article_id__id=article_pk #公開の記事のみ
        ).all().order_by('order_id')

        str_Html = '<h2>' + obj.intro_title + '</h2>'
        str_Html += obj.intro_content

        logger.debug(obj.intro_title)
        logger.debug(obj.intro_content)

        for detail_obj in objdetail:
            str_Html += '<h3>' + detail_obj.block_title + '</h3>'
            str_Html += detail_obj.block_content

            logger.debug(detail_obj.block_title)
            logger.debug(detail_obj.block_content)

        context['html_pre'] = str_Html

        return context


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







class CategoryFilterView(LoginRequiredMixin, FilterView):
    model = Category
    filterset_class = CategoryFilterSet

    queryset = Category.objects.all().order_by('-created_at')

    # 1ページの表示
    paginate_by = 10
    object = Category

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

class CategoryCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/category_form.html'
    model = Category
    form_class = CategoryForm


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    is_update_view = True
    template_name = 'article/category_form.html'
    model = Category
    form_class = CategoryForm


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category')

class CategoryDetailView(LoginRequiredMixin, DetailView):

    model = Category


"""/comment/post_pk コメント投稿."""
class CommentView(generic.CreateView):    
    model = Comment
    fields = '__all__'
    template_name = 'article/article_comment_form.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['initial'] = {'target': self.kwargs['pk']}  # フォームに初期値を設定する。
        return form_kwargs 

    def form_valid(self, form):
        article_pk = self.kwargs['pk']
        article = get_object_or_404(Article, pk=article_pk)
        # 紐づく記事を設定する
        comment = form.save(commit=False)
        comment.target = article
        comment.save()
 
        # 記事詳細にリダイレクト
        #return redirect(article.get_absolute_url())
        return redirect('detail', pk=article_pk)



"""/reply/comment_pk 返信コメント投稿."""
class ReplyView(generic.CreateView):
    model = Reply
    fields = '__all__'
    template_name = 'article/article_comment_form.html'

    def form_valid(self, form):
        
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
 
        # 紐づくコメントを設定する
        reply = form.save(commit=False)
        reply.target = comment
        reply.save()
 
        # 記事詳細にリダイレクト
        #return redirect('detail', pk=article.id)
        return redirect('detail', pk=self.kwargs['pk'])