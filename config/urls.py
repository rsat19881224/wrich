
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ルーティング設定
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('article.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 管理サイトの見出しを変更可能
#  タイトル；タイトルタグで使用
admin.site.site_title = 'タイトル'
#  サイト名：ログイン画面と管理画面上部の表示
admin.site.site_header = 'wrich(記事入稿)'
#  メニュー：管理画面の見出し表示
admin.site.index_title = '管理メニュー'

#django-debug-toolbar用
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]