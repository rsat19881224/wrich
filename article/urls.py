from django.urls import path

from . import views
# アプリケーションのルーティング設定

urlpatterns = [
    path('myboard/', views.MyboardView.as_view(), name='myboard'),
    path('', views.ArticleFilterView.as_view(), name='index'),
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('create/', views.ArticleCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.ArticleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete'),

    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment'),
    path('comment/update/<int:pk>/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('reply/<int:pk>/', views.ReplyView.as_view(), name='reply'),
    path('reply/update/<int:pk>/', views.ReplyUpdateView.as_view(), name='reply_update'),

    path('category/', views.CategoryFilterView.as_view(), name='category'),
    path('category/detail/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('site/', views.SiteFilterView.as_view(), name='site'),
    path('site/detail/<int:pk>/', views.SiteDetailView.as_view(), name='site_detail'),
    path('site/create/', views.SiteCreateView.as_view(), name='site_create'),
    path('site/update/<int:pk>/', views.SiteUpdateView.as_view(), name='site_update'),
    path('site/delete/<int:pk>/', views.SiteDeleteView.as_view(), name='site_delete'),

    path('order/', views.OrderFilterView.as_view(), name='order'),
    path('order/detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order/update/<int:pk>/', views.OrderUpdateView.as_view(), name='order_update'),
    path('order/delete/<int:pk>/', views.OrderDeleteView.as_view(), name='order_delete'),

    path('info/', views.InfoFilterView.as_view(), name='info'),
    path('info/detail/<int:pk>/', views.InfoDetailView.as_view(), name='info_detail'),
    path('info/create/', views.InfoCreateView.as_view(), name='info_create'),
    path('info/update/<int:pk>/', views.InfoUpdateView.as_view(), name='info_update'),
    path('info/delete/<int:pk>/', views.InfoDeleteView.as_view(), name='info_delete'),

    path('image/', views.ImageFilterView.as_view(), name='image'),
    path('image/upload/', views.upload, name='image_upload'),
    path('image/detail/<int:pk>/', views.image, name='image_detail'),
]