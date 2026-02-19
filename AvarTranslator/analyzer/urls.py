from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='analyzer_index'),
    path('api/analyze/', views.analyze_api, name='analyze_api'),
    path('test/', views.test_analysis, name='test_analysis'),
]