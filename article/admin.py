from django.contrib import admin

from .models import Article, ArticleDetail, Comment, Reply, Category, Site, Order, Info


class ArticleDetailInline(admin.TabularInline):
    model = ArticleDetail
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleDetailInline]

admin.site.register(Site)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Info)