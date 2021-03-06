from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404,render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import DetailView,TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from logging import getLogger
logger = getLogger(__name__)

import requests
from django.views.decorators.http import require_GET, require_http_methods

from .filters import ArticleFilterSet, CategoryFilterSet, SiteFilterSet, OrderFilterSet, InfoFilterSet, ImageFilterSet
from .forms import ArticleForm, ArticleDetailFormSet, CommentForm, ReplyForm, CategoryForm, SiteForm, OrderForm, InfoForm, ImageForm
from .models import Article, ArticleDetail, ArticleFix, Comment, Reply, Category, Site, Order, Info, Image

#Chatwork連携用
CHATWORK_API_TOKEN = '5b9460499bb66c1b61f650eeccbc08dd' #R mytoken
CHATWORK_API_ROOM_ID = '81445055' #R mytalk
CHATWORK_API_ENDPOINT_BASE = 'https://api.chatwork.com/v2'
CHATWORK_API_BACKEND = 'chatwork.backends.http.UrllibBackend' 
CHATWORK_API_FAIL_SILENTLY = None   # default


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

            message  = '[info][title]さんが記事を作成しました。'
            #message  += '[/title]' + 'タイトル:' + article.intro_title + 'pk:' + article.pk + '[/info]' 
            #message  = '[info][title]' + self.request.user.get_username + 'さんが記事を作成しました。'

            post_message_url = '{}/rooms/{}/messages'.format(CHATWORK_API_ENDPOINT_BASE, CHATWORK_API_ROOM_ID)
            headers = { 'X-ChatWorkToken': CHATWORK_API_TOKEN}
            params = { 'body': message }
            r = requests.post(post_message_url,headers=headers,params=params)
            print(r)

            messages.success(self.request, f'記事を作成しました。 タイトル:{article.intro_title} pk:{article.pk}'.format(form.instance))
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

        for detail_obj in objdetail:
            str_Html += '<h3>' + detail_obj.block_title + '</h3>'
            str_Html += detail_obj.block_content
            #context['fix_list'] = ArticleFix.objects.filter(articledetail=detail_obj.id)

        context['html_pre'] = str_Html
        context['html_len'] = '{:,}'.format(len(str_Html))

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

#####################################################
#
#
"""指摘投稿."""
class ArticleFixView(generic.CreateView):    
    model = ArticleFix
    fields = ('block_fix',)
    template_name = 'article/article_fix_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_list'] = ArticleDetail.objects.filter(id=self.kwargs['pk'])
        
        return context

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['initial'] = {'articledetail': self.kwargs['pk']}  # フォームに初期値を設定する。
        
        return form_kwargs 

    def form_valid(self, form):
        articledetail_pk = self.kwargs['pk']
        articledetail = get_object_or_404(ArticleDetail, pk=articledetail_pk)
        # 紐づく記事を設定する
        articlefix = form.save(commit=False)
        articlefix.articledetail = articledetail
        articlefix.save()
 
        # 記事詳細にリダイレクト
        #return redirect(article.get_absolute_url())
        return redirect('detail', pk=self.kwargs['pk'])


#####################################################
#
#
class MyboardView(TemplateView):
    template_name = 'article/Myboard.html'

    #@cached_property
    #def info(self):
    #    """所持アイテム一覧"""
    #    return Info.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info_list'] = Info.objects.all().order_by('-created_at')
        context['user_orders'] = Order.objects.filter(order_user=self.request.user).order_by('-created_at')
        context['user_articles'] = Article.objects.filter(created_by=self.request.user).order_by('-created_at')
        context['user_comments'] = Comment.objects.filter(created_by=self.request.user).order_by('-created_at')
        context['user_imgages'] = Image.objects.filter(created_by=self.request.user).order_by('-created_at')

        return context

#####################################################
#
#
class SiteFilterView(LoginRequiredMixin, FilterView):
    model = Site
    filterset_class = SiteFilterSet

    queryset = Site.objects.all().order_by('-created_at')

    # 1ページの表示
    paginate_by = 10
    object = Site

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

class SiteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/site_form.html'
    model = Site
    form_class = SiteForm


class SiteUpdateView(LoginRequiredMixin, UpdateView):
    is_update_view = True
    template_name = 'article/site_form.html'
    model = Site
    form_class = SiteForm


class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = Site
    success_url = reverse_lazy('site')

class SiteDetailView(LoginRequiredMixin, DetailView):

    model = Site


#####################################################
#
#
class OrderFilterView(LoginRequiredMixin, FilterView):
    model = Order
    filterset_class = OrderFilterSet

    queryset = Order.objects.all().order_by('-created_at')

    # 1ページの表示
    paginate_by = 10
    object = Order

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

class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/order_form.html'
    model = Order
    form_class = OrderForm


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    is_update_view = True
    template_name = 'article/order_form.html'
    model = Order
    form_class = OrderForm


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order')

class OrderDetailView(LoginRequiredMixin, DetailView):

    model = Order


#####################################################
#
#
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

#####################################################
#
#
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

class CommentUpdateView(generic.UpdateView):
    template_name = 'article/article_comment_form.html'
    model = Comment
    fields = '__all__'
    
    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, 'コメントを「{}」に更新しました'.format(form.instance))
        return result


"""/reply/comment_pk 返信コメント投稿."""
class ReplyView(generic.CreateView):
    model = Reply
    fields = '__all__'
    template_name = 'article/article_comment_form.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['initial'] = {'target': self.kwargs['pk']}  # フォームに初期値を設定する。
        return form_kwargs 

    def form_valid(self, form):
        
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)

        #art_comment = Comment.objects.select_related('target').filter(pk=comment_pk)
        #logger.debug(art_comment)

        # 紐づくコメントを設定する
        reply = form.save(commit=False)
        reply.target = comment
        reply.save()
 
        # 記事詳細にリダイレクト
        #return redirect('detail', pk=article.id)
        return redirect('detail', pk=1)

class ReplyUpdateView(generic.UpdateView):
    template_name = 'article/article_comment_form.html'
    model = Reply
    fields = '__all__'
    
    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '返信コメントを「{}」に更新しました'.format(form.instance))
        return result

class InfoFilterView(LoginRequiredMixin, FilterView):
    model = Info
    filterset_class = InfoFilterSet

    queryset = Info.objects.all().order_by('-created_at')

    # 1ページの表示
    paginate_by = 10
    object = Info

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

class InfoCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/info_form.html'
    model = Info
    form_class = InfoForm


class InfoUpdateView(LoginRequiredMixin, UpdateView):
    is_update_view = True
    template_name = 'article/info_form.html'
    model = Info
    form_class = InfoForm


class InfoDeleteView(LoginRequiredMixin, DeleteView):
    model = Info
    success_url = reverse_lazy('info')

class InfoDetailView(LoginRequiredMixin, DetailView):

    model = Info




class ImageFilterView(LoginRequiredMixin, FilterView):
    model = Image
    filterset_class = ImageFilterSet

    queryset = Image.objects.all().order_by('-created_at')

    # 1ページの表示
    paginate_by = 10
    object = Image

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


@require_GET
def image(request):
    image = Image.objects.get(id=self.kwargs['pk'])
    return render(request, 'article/Image_detail.html', {'image': image})

@require_GET
def image_list(request):
    images = Image.objects.all()
    return render(request, 'article/Image_list.html', {'images': images})


@require_http_methods(["GET", "POST"])
def upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/image/')
    else:
        form = ImageForm()
    return render(request, 'article/Image_upload.html', {'form': form})



class UserView(TemplateView):
    template_name = 'article/user_info.html'

    #@cached_property
    #def info(self):
    #    """所持アイテム一覧"""
    #    return Info.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info_list'] = Info.objects.all().order_by('-created_at')
        context['user_orders'] = Order.objects.filter(order_user=self.request.user).order_by(-created_at)
        context['user_articles'] = Article.objects.filter(created_by=self.request.user).order_by(-created_at)
        context['user_comments'] = Comment.objects.filter(created_by=self.request.user).order_by(-created_at)
        context['user_imgages'] = Image.objects.filter(created_by=self.request.user).order_by(-created_at)

        #ユーザー別、未払い件数のおよび金額の表示、依頼サイトorサービスグループ化？

        return context
