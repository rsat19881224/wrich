from django.urls import path

from article import views
# アプリケーションのルーティング設定

urlpatterns = [
    path('', views.ArticleFilterView.as_view(), name='index'),
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('create/', views.ArticleCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.ArticleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete'),
]