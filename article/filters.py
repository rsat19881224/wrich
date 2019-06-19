import django_filters
from django.db import models

from .models import Article, Category, Site, Order, Info


class OrderingFilter(django_filters.filters.OrderingFilter):
    """日本語対応"""
    descending_fmt = '%s （降順）'


class ArticleFilterSet(django_filters.FilterSet):
    """
     django-filter 構成クラス
    https://django-filter.readthedocs.io/en/latest/ref/filterset.html
    """

    # 検索フォームの「並び順」の設定
    order_by = OrderingFilter(
        initial='作成日',
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'created_at': '作成日',
            'updated_at': '更新日',
        },
        label='並び順'
    )

    class Meta:
        model = Article
        # 一部フィールドを除きモデルクラスの定義を全て引用する
        exclude = ['created_at', 'updated_by', 'updated_at', ]
        # 文字列検索のデフォルトを部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

class SiteFilterSet(django_filters.FilterSet):
    # 検索フォームの「並び順」の設定
    order_by = OrderingFilter(
        initial='作成日',
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'created_at': '作成日',
            'updated_at': '更新時間',
        },
        label='並び順'
    )

    class Meta:
        model = Site
        # 一部フィールドを除きモデルクラスの定義を全て引用する
        exclude = ['created_at', 'updated_by', 'updated_at', ]
        # 文字列検索のデフォルトを部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

class OrderFilterSet(django_filters.FilterSet):
    # 検索フォームの「並び順」の設定
    order_by = OrderingFilter(
        initial='作成日',
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'created_at': '作成日',
            'updated_at': '更新時間',
        },
        label='並び順'
    )

    class Meta:
        model = Order
        # 一部フィールドを除きモデルクラスの定義を全て引用する
        exclude = ['created_at', 'updated_by', 'updated_at', ]
        # 文字列検索のデフォルトを部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

class CategoryFilterSet(django_filters.FilterSet):
    order_by = OrderingFilter(
        initial='作成日',
        fields=(
            ('created_at', 'created_at'),
        ),
        field_labels={
            'created_at': '作成日',
        },
        label='並び順'
    )
    class Meta:
        model = Category
        fields = ('name', 'description', 'created_by','created_at',)
        # 文字列検索のデフォルトを部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

class InfoFilterSet(django_filters.FilterSet):
    order_by = OrderingFilter(
        initial='作成日',
        fields=(
            ('created_at', 'created_at'),
        ),
        field_labels={
            'created_at': '作成日',
        },
        label='並び順'
    )
    class Meta:
        model = Info
        fields = ('note', 'target_group', 'public_date','close_date','created_by','created_at',)
        # 文字列検索のデフォルトを部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }