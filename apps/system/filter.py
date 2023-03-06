import django_filters

from apps.system.models import SysMenu


class SysMenuFilter(django_filters.rest_framework.FilterSet):
    # lookup_expr='icontains' 包含
    s_platform = django_filters.NumberFilter(field_name='platform')
    top_category = django_filters.NumberFilter(method='top_category_filter')


    class Meta:
        model = SysMenu
        fields = ['platform']


    def top_category_filter(self, queryset, name, value):

        return None