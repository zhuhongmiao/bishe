from rest_framework import serializers

from apps.fabric.models import Fabric
from apps.manage.models import AdminNotification, AdminOperationLog, AdminSystemConfig
from apps.user.models import User


def normalize_bool(value):
    if isinstance(value, bool):
        return value
    if value in ['true', 'True', '1', 1, 'on']:
        return True
    if value in ['false', 'False', '0', 0, 'off']:
        return False
    return value


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'is_admin',
            'is_staff',
            'is_active',
            'last_login',
            'email',
            'phone_number',
        ]
        read_only_fields = ['id', 'last_login']

    def validate_username(self, value):
        queryset = User.objects.filter(username=value)
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise serializers.ValidationError('用户名已存在')
        return value

    def validate_email(self, value):
        if value in [None, '']:
            return None
        queryset = User.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise serializers.ValidationError('邮箱已存在')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if 'is_admin' in validated_data:
            validated_data['is_admin'] = normalize_bool(validated_data['is_admin'])
        if 'is_staff' in validated_data:
            validated_data['is_staff'] = normalize_bool(validated_data['is_staff'])
        if 'is_active' in validated_data:
            validated_data['is_active'] = normalize_bool(validated_data['is_active'])
        if validated_data.get('email', '') == '':
            validated_data['email'] = None
        if validated_data.get('phone_number', '') == '':
            validated_data['phone_number'] = None

        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            raise serializers.ValidationError({'password': '密码不能为空'})
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if 'is_admin' in validated_data:
            validated_data['is_admin'] = normalize_bool(validated_data['is_admin'])
        if 'is_staff' in validated_data:
            validated_data['is_staff'] = normalize_bool(validated_data['is_staff'])
        if 'is_active' in validated_data:
            validated_data['is_active'] = normalize_bool(validated_data['is_active'])
        if validated_data.get('email', '') == '':
            validated_data['email'] = None
        if validated_data.get('phone_number', '') == '':
            validated_data['phone_number'] = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AdminFabricSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    pattern = serializers.SerializerMethodField()

    class Meta:
        model = Fabric
        fields = [
            'id',
            'title',
            'category_name',
            'category_id',
            'weight',
            'country',
            'price',
            'pattern',
            'like',
            'is_visible',
            'is_recommended',
            'is_available',
        ]
        read_only_fields = ['id']

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('面料名称不能为空')
        return value.strip()

    def get_title(self, obj):
        return obj.translate_text(obj.title)

    def get_category_name(self, obj):
        return obj.translate_text(obj.category_name)

    def get_country(self, obj):
        return obj.translate_text(obj.country)

    def get_pattern(self, obj):
        return obj.translate_text(obj.pattern)


class AdminOperationLogSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.username', read_only=True)

    class Meta:
        model = AdminOperationLog
        fields = '__all__'


class AdminSystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSystemConfig
        fields = '__all__'


class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotification
        fields = '__all__'


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, allow_blank=False)


class BatchIdsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)


class BatchFabricStatusSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    is_visible = serializers.BooleanField(required=False)
    is_recommended = serializers.BooleanField(required=False)
    is_available = serializers.BooleanField(required=False)
