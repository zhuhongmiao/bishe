from django.urls import path,include
from rest_framework.routers import DefaultRouter
import apps.fabric.views as views

router = DefaultRouter()
router.register(r'fabrics', views.FabricViewSet, basename='fabrics')

urlpatterns = [
    path('/', include(router.urls)),
    path('/options/', views.FabricFieldOptionsView.as_view(), name='fabric-options'),
    path('/manage', views.FabricManage.as_view(), name='fabric-manage'),
]