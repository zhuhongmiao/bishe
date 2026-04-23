# apps/fabric/filters.py
import django_filters as f
from .models import Fabric

class FabricFilter(f.FilterSet):
    # 模糊匹配
    title = f.CharFilter(field_name='title', lookup_expr='icontains')
    category_name = f.CharFilter(field_name='category_name', lookup_expr='icontains')
    country = f.CharFilter(field_name='country', lookup_expr='icontains')
    pattern = f.CharFilter(field_name='pattern', lookup_expr='icontains')

    # 区间过滤（价格、重量）
    min_price = f.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = f.NumberFilter(field_name='price', lookup_expr='lte')
    min_weight = f.NumberFilter(field_name='weight', lookup_expr='gte')
    max_weight = f.NumberFilter(field_name='weight', lookup_expr='lte')

    class Meta:
        model = Fabric
        fields = [
            'title', 'category_name', 'country', 'pattern',
            'min_price', 'max_price', 'min_weight', 'max_weight'
        ]
