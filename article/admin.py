from django.contrib import admin

from .models import Article, ArticleDetail


class ArticleDetailInline(admin.TabularInline):
    model = ArticleDetail
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleDetailInline]