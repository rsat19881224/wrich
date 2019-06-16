from django.urls import path

from . import views
# アプリケーションのルーティング設定

urlpatterns = [
    path('', views.ArticleFilterView.as_view(), name='index'),
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('create/', views.ArticleCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.ArticleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete'),
    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment'),
    path('reply/<int:pk>/', views.ReplyView.as_view(), name='reply'),
    path('category/', views.CategoryFilterView.as_view(), name='category'),
    path('category/detail/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
]