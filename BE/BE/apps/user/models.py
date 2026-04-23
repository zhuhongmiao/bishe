# from django.db import models
# from django.contrib.auth.hashers import make_password, check_password

# # Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=128)
#     is_admin = models.BooleanField(default=False)

#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []
# apps/user/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_admin=False, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, is_admin=is_admin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True")
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)   # 用于 admin 后台权限
    is_active = models.BooleanField(default=True)   # 是否可用（禁用账户时用）
    # 新增字段
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # 创建超级用户时额外需要的字段（不包括 USERNAME_FIELD）

    objects = UserManager()

    def __str__(self):
        return self.username
