from django.urls import path

import apps.user.views as views

urlpatterns = [
    path('', views.UserView.as_view(), name='user'),
    path('/login', views.LoginView.as_view(), name='login'),
    path('/token/verify', views.VerboseTokenVerifyView.as_view(), name='token-verify'),
    path('/manage', views.UserManageView.as_view(), name='user-manage'),
]