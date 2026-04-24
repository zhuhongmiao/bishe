from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView

from apps.common.pagination import StandardPageNumberPagination
from apps.fabric.models import Fabric
from apps.manage.serializers import (
    AdminFabricSerializer,
    AdminUserSerializer,
    BatchFabricStatusSerializer,
    BatchIdsSerializer,
    ResetPasswordSerializer,
)
from apps.user.models import User
from utils.responseMessage import ResponseMessage


class IsAdminManageUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_admin or user.is_staff or user.is_superuser))


class DashboardOverviewView(APIView):
    permission_classes = [IsAdminManageUser]

    def get(self, request):
        data = {
            'total_users': User.objects.count(),
            'total_admin_users': User.objects.filter(is_admin=True).count(),
            'total_fabrics': Fabric.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
        }
        return ResponseMessage.success(data)


class AdminUserManageView(APIView):
    permission_classes = [IsAdminManageUser]

    def get(self, request):
        keyword = request.query_params.get('keyword', '').strip()
        is_admin = request.query_params.get('is_admin')
        is_active = request.query_params.get('is_active')

        queryset = User.objects.all().order_by('-id')
        if keyword:
            queryset = queryset.filter(
                Q(username__icontains=keyword)
                | Q(email__icontains=keyword)
                | Q(phone_number__icontains=keyword)
            )
        if is_admin in ['true', 'false']:
            queryset = queryset.filter(is_admin=(is_admin == 'true'))
        if is_active in ['true', 'false']:
            queryset = queryset.filter(is_active=(is_active == 'true'))

        paginator = StandardPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = AdminUserSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        payload = request.data.copy()
        if 'is_staff' not in payload:
            payload['is_staff'] = payload.get('is_admin', False)
        serializer = AdminUserSerializer(data=payload)
        if not serializer.is_valid():
            return ResponseMessage.failed('用户新增失败', data=serializer.errors)
        serializer.save()
        return ResponseMessage.success(serializer.data, msg='用户新增成功')


class AdminUserDetailView(APIView):
    permission_classes = [IsAdminManageUser]

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, user_id):
        user = self.get_object(user_id)
        if not user:
            return ResponseMessage.failed('用户不存在')
        serializer = AdminUserSerializer(user)
        return ResponseMessage.success(serializer.data)

    def put(self, request, user_id):
        user = self.get_object(user_id)
        if not user:
            return ResponseMessage.failed('用户不存在')
        payload = request.data.copy()
        if 'is_admin' in payload and 'is_staff' not in payload:
            payload['is_staff'] = payload.get('is_admin')
        serializer = AdminUserSerializer(user, data=payload, partial=True)
        if not serializer.is_valid():
            return ResponseMessage.failed('用户更新失败', data=serializer.errors)
        serializer.save()
        return ResponseMessage.success(serializer.data, msg='用户更新成功')

    def delete(self, request, user_id):
        user = self.get_object(user_id)
        if not user:
            return ResponseMessage.failed('用户不存在')
        if user.id == request.user.id:
            return ResponseMessage.failed('不能删除当前登录管理员')
        if user.is_admin and User.objects.filter(is_admin=True).count() <= 1:
            return ResponseMessage.failed('不能删除最后一个管理员')
        user.delete()
        return ResponseMessage.success({}, msg='用户删除成功')


class AdminUserResetPasswordView(APIView):
    permission_classes = [IsAdminManageUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return ResponseMessage.failed('用户不存在')
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseMessage.failed('重置密码失败', data=serializer.errors)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return ResponseMessage.success({}, msg='密码重置成功')


class AdminUserBatchActionView(APIView):
    permission_classes = [IsAdminManageUser]

    def post(self, request):
        action = request.data.get('action')
        ids_serializer = BatchIdsSerializer(data={'ids': request.data.get('ids', [])})
        if not ids_serializer.is_valid():
            return ResponseMessage.failed('批量操作失败', data=ids_serializer.errors)
        ids = ids_serializer.validated_data['ids']
        queryset = User.objects.filter(id__in=ids)

        if action == 'delete':
            if request.user.id in ids:
                return ResponseMessage.failed('不能删除当前登录管理员')
            admin_delete_count = queryset.filter(is_admin=True).count()
            if admin_delete_count and User.objects.filter(is_admin=True).count() <= admin_delete_count:
                return ResponseMessage.failed('不能删除全部管理员')
            count = queryset.count()
            queryset.delete()
            return ResponseMessage.success({'count': count}, msg='批量删除成功')

        if action == 'enable':
            count = queryset.update(is_active=True)
            return ResponseMessage.success({'count': count}, msg='批量启用成功')

        if action == 'disable':
            if request.user.id in ids:
                return ResponseMessage.failed('不能禁用当前登录管理员')
            admin_disable_count = queryset.filter(is_admin=True).count()
            if admin_disable_count and User.objects.filter(is_admin=True, is_active=True).count() <= admin_disable_count:
                return ResponseMessage.failed('不能禁用全部管理员')
            count = queryset.update(is_active=False)
            return ResponseMessage.success({'count': count}, msg='批量禁用成功')

        return ResponseMessage.failed('不支持的批量操作')


class AdminFabricManageView(APIView):
    permission_classes = [IsAdminManageUser]

    def get(self, request):
        keyword = request.query_params.get('keyword', '').strip()
        category_name = request.query_params.get('category_name', '').strip()
        country = request.query_params.get('country', '').strip()
        pattern = request.query_params.get('pattern', '').strip()
        is_visible = request.query_params.get('is_visible')
        is_recommended = request.query_params.get('is_recommended')
        is_available = request.query_params.get('is_available')
        ordering = request.query_params.get('ordering', 'id').strip()

        allowed_orderings = {'id', '-id', 'price', '-price', 'weight', '-weight', 'like', '-like'}
        if ordering not in allowed_orderings:
            ordering = 'id'

        queryset = Fabric.objects.all().order_by(ordering)
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                | Q(category_name__icontains=keyword)
                | Q(country__icontains=keyword)
                | Q(pattern__icontains=keyword)
            )
        if category_name:
            queryset = queryset.filter(category_name__icontains=category_name)
        if country:
            queryset = queryset.filter(country__icontains=country)
        if pattern:
            queryset = queryset.filter(pattern__icontains=pattern)
        if is_visible in ['true', 'false']:
            queryset = queryset.filter(is_visible=(is_visible == 'true'))
        if is_recommended in ['true', 'false']:
            queryset = queryset.filter(is_recommended=(is_recommended == 'true'))
        if is_available in ['true', 'false']:
            queryset = queryset.filter(is_available=(is_available == 'true'))

        paginator = StandardPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = AdminFabricSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = AdminFabricSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseMessage.failed('面料新增失败', data=serializer.errors)
        serializer.save()
        return ResponseMessage.success(serializer.data, msg='面料新增成功')


class AdminFabricDetailView(APIView):
    permission_classes = [IsAdminManageUser]

    def get_object(self, fabric_id):
        try:
            return Fabric.objects.get(id=fabric_id)
        except Fabric.DoesNotExist:
            return None

    def get(self, request, fabric_id):
        fabric = self.get_object(fabric_id)
        if not fabric:
            return ResponseMessage.failed('面料不存在')
        serializer = AdminFabricSerializer(fabric)
        return ResponseMessage.success(serializer.data)

    def put(self, request, fabric_id):
        fabric = self.get_object(fabric_id)
        if not fabric:
            return ResponseMessage.failed('面料不存在')
        serializer = AdminFabricSerializer(fabric, data=request.data, partial=True)
        if not serializer.is_valid():
            return ResponseMessage.failed('面料更新失败', data=serializer.errors)
        serializer.save()
        return ResponseMessage.success(serializer.data, msg='面料更新成功')

    def delete(self, request, fabric_id):
        fabric = self.get_object(fabric_id)
        if not fabric:
            return ResponseMessage.failed('面料不存在')
        fabric.delete()
        return ResponseMessage.success({}, msg='面料删除成功')


class AdminFabricBatchActionView(APIView):
    permission_classes = [IsAdminManageUser]

    def post(self, request):
        action = request.data.get('action')
        ids = request.data.get('ids', [])

        if action == 'delete':
            serializer = BatchIdsSerializer(data={'ids': ids})
            if not serializer.is_valid():
                return ResponseMessage.failed('批量删除失败', data=serializer.errors)
            queryset = Fabric.objects.filter(id__in=serializer.validated_data['ids'])
            count = queryset.count()
            queryset.delete()
            return ResponseMessage.success({'count': count}, msg='批量删除成功')

        serializer = BatchFabricStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseMessage.failed('批量更新失败', data=serializer.errors)
        data = serializer.validated_data
        ids = data.pop('ids')
        count = Fabric.objects.filter(id__in=ids).update(**data)
        return ResponseMessage.success({'count': count}, msg='批量更新成功')
