from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MorphemeViewSet, TagViewSet

router = DefaultRouter()
router.register(r'morphemes', MorphemeViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]