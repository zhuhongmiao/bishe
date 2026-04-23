from django.urls import path

import apps.analysis.views as views

urlpatterns = [
    # path('', views.UserView.as_view(), name='user'),
    # path('/login', views.LoginView.as_view(), name='login'),
    # path('/token/verify', views.VerboseTokenVerifyView.as_view(), name='token-verify'),
    path('/countries', views.get_countries, name='countries'),
    path('/price-stats', views.price_statistics, name='price-stats'),
    path('/price-predict-options', views.price_predict_options, name='price-predict-options'),
    path('/category-price-boxplot', views.category_price_boxplot_echarts, name='category-price-boxplot'),
    path('/pattern-price-boxplot', views.pattern_price_boxplot_echarts, name='pattern-price-boxplot'),
    path('/clustering-analysis', views.clustering_analysis, name='clustering-analysis'),
    path('/price-prediction-model', views.price_prediction_model, name='price-prediction-model'),
    path('/price-predict', views.price_predict_single, name='price-predict'),
    path('/ai-chat', views.ai_chat_with_data, name='ai-chat'),
    path('/ai-chat-stream', views.ai_chat_with_data_stream, name='ai-chat-stream'),
]