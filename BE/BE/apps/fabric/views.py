# apps/febric/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from utils.responseMessage import ResponseMessage
from .models import Fabric
from .serializers import FabricSerializer
from .filters import FabricFilter
from apps.common.pagination import StandardPageNumberPagination  # 请参考下方完整分页类
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class FabricViewSet(viewsets.ReadOnlyModelViewSet):
    """
    一个支持：
    - 模糊查询（title/category_name/country/pattern）
    - 区间过滤（min_price/max_price/min_weight/max_weight）
    - 排序（价格、重量、点赞数等）
    - 分页（page & page_size）
    的接口

    请求示例：
    /api/febrics/?title=lac&country=Korea&min_price=10&max_price=50&ordering=-price&page=2&page_size=20
    """
    permission_classes = [AllowAny]

    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer
    pagination_class = StandardPageNumberPagination

    # 允许使用的过滤和排序
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FabricFilter
    ordering_fields = ['price', 'weight', 'like', 'id']  # 可排序字段
    ordering = ['id']  # 默认排序方式

class FabricFieldOptionsView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        filed=request.query_params.get('field')
        allowed_fields=['category_name','country','pattern']
        if filed not in allowed_fields:
            return ResponseMessage.failed("Invalid field")

        values = Fabric.objects.values_list(filed, flat=True).distinct().order_by(filed)
        return ResponseMessage.success(list(values))
class FabricManage(APIView):
    def put(self,request):
        id=request.data.get('id')
        title=request.data.get('title')
        category_name=request.data.get('category_name')
        country=request.data.get('country')
        pattern=request.data.get('pattern')
        price=request.data.get('price')
        if id is None or title is None or category_name is None or country is None or pattern is None or price is None:
            return ResponseMessage.failed("缺少必填参数")
        try:
            fabric=Fabric.objects.get(id=id)
        except Fabric.DoesNotExist:
            return ResponseMessage.failed("面料不存在")
        fabric.title=title
        fabric.category_name=category_name
        fabric.country=country
        fabric.pattern=pattern
        fabric.price=price
        fabric.save()
        return ResponseMessage.success({},msg="面料信息更新成功")
    def delete(self,request):
        id=request.data.get('id')
        if id is None:
            return ResponseMessage.failed("id 必填")
        try:
            fabric=Fabric.objects.get(id=id)
        except Fabric.DoesNotExist:
            return ResponseMessage.failed("面料不存在")
        fabric.delete()
        return ResponseMessage.success({},msg="面料删除成功")