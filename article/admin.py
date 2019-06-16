from django.contrib import admin

from .models import Article, ArticleDetail, Comment, Reply, Category


class ArticleDetailInline(admin.TabularInline):
    model = ArticleDetail
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleDetailInline]

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Category)