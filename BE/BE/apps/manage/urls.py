from django.urls import path

from apps.manage import views

urlpatterns = [
    path('/overview', views.DashboardOverviewView.as_view(), name='manage-overview'),
    path('/overview/', views.DashboardOverviewView.as_view()),
    path('/users', views.AdminUserManageView.as_view(), name='manage-users'),
    path('/users/', views.AdminUserManageView.as_view()),
    path('/users/batch', views.AdminUserBatchActionView.as_view(), name='manage-users-batch'),
    path('/users/batch/', views.AdminUserBatchActionView.as_view()),
    path('/users/<int:user_id>', views.AdminUserDetailView.as_view(), name='manage-user-detail'),
    path('/users/<int:user_id>/', views.AdminUserDetailView.as_view()),
    path('/users/<int:user_id>/reset-password', views.AdminUserResetPasswordView.as_view(), name='manage-user-reset-password'),
    path('/users/<int:user_id>/reset-password/', views.AdminUserResetPasswordView.as_view()),
    path('/fabrics', views.AdminFabricManageView.as_view(), name='manage-fabrics'),
    path('/fabrics/', views.AdminFabricManageView.as_view()),
    path('/fabrics/batch', views.AdminFabricBatchActionView.as_view(), name='manage-fabrics-batch'),
    path('/fabrics/batch/', views.AdminFabricBatchActionView.as_view()),
    path('/fabrics/<int:fabric_id>', views.AdminFabricDetailView.as_view(), name='manage-fabric-detail'),
    path('/fabrics/<int:fabric_id>/', views.AdminFabricDetailView.as_view()),
]
