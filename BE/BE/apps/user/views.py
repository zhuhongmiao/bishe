from rest_framework.views import APIView
from .models import User
from utils.responseMessage import ResponseMessage
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from django.utils import timezone


class UserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        is_admin = request.data.get('is_admin', False)
        email = request.data.get('email', None)
        phone_number = request.data.get('phone_number', None)
        try:
            User.objects.get(username=username)
            return ResponseMessage.failed('用户名已存在')
        except User.DoesNotExist:
            user = User(
                username=username,
                is_admin=is_admin,
                is_staff=is_admin,
                email=email,
                phone_number=phone_number,
            )
            user.set_password(password)
            user.save()
            return ResponseMessage.success({}, msg='注册成功！')


class UserManageView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        if username:
            users = User.objects.filter(username__icontains=username)
            if users.count() == 0:
                return ResponseMessage.failed('用户不存在')
            data = [
                {
                    'id': user.id,
                    'username': user.username,
                    'is_admin': user.is_admin,
                    'last_login': user.last_login,
                    'email': user.email,
                    'phone_number': user.phone_number,
                }
                for user in users
            ]
            return ResponseMessage.success(data)
        users = User.objects.all()
        data = [
            {
                'id': user.id,
                'username': user.username,
                'is_admin': user.is_admin,
                'last_login': user.last_login,
                'email': user.email,
                'phone_number': user.phone_number,
            }
            for user in users
        ]
        return ResponseMessage.success(data)

    def put(self, request):
        user_id = request.data.get('id')
        username = request.data.get('username')
        is_admin = request.data.get('is_admin')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')

        if user_id is None or is_admin is None or username is None:
            return ResponseMessage.failed('id 和 is_admin 和 username 必填')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return ResponseMessage.failed('用户不存在')
        user.username = username
        user.is_admin = is_admin
        user.is_staff = is_admin
        user.email = email
        user.phone_number = phone_number
        user.save(update_fields=['username', 'is_admin', 'is_staff', 'email', 'phone_number'])
        return ResponseMessage.success({}, msg='更新成功')

    def delete(self, request):
        user_id = request.data.get('id')
        if user_id is None:
            return ResponseMessage.failed('id 必填')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return ResponseMessage.failed('用户不存在')
        user.delete()
        return ResponseMessage.success({}, msg='删除成功')


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return ResponseMessage.failed('username 和 password 必填')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return ResponseMessage.failed('用户或密码错误')

        if not user.check_password(password):
            return ResponseMessage.failed('用户或密码错误')
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        refresh = RefreshToken.for_user(user)
        data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'is_admin': user.is_admin,
                'email': user.email,
                'phone_number': user.phone_number,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return ResponseMessage.success(data)


class VerboseTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        super().validate(attrs)
        token = UntypedToken(attrs['token'])
        user = User.objects.get(id=token.get('user_id'))
        return {
            'id': user.id,
            'username': user.username,
            'is_admin': user.is_admin,
            'email': user.email,
            'phone_number': user.phone_number,
        }


class VerboseTokenVerifyView(TokenVerifyView):
    serializer_class = VerboseTokenVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return ResponseMessage.success(serializer.validated_data)
        except Exception:
            return ResponseMessage.failed('Token invalid or expired')
