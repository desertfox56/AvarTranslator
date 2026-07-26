from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Morpheme, Tag
from .serializers import MorphemeSerializer, TagSerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """API для просмотра всех тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class MorphemeViewSet(viewsets.ReadOnlyModelViewSet):
    """API для работы с морфемами"""
    queryset = Morpheme.objects.all()
    serializer_class = MorphemeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Получаем параметры из URL
        surface_query = self.request.query_params.get('surface', None)
        tag_query = self.request.query_params.get('tag', None)

        # Фильтр по тексту
        if surface_query is not None:
            queryset = queryset.filter(surface__icontains=surface_query)
            
        # Фильтр по грамматическому тегу 
        if tag_query is not None:
            
            queryset = queryset.filter(adds_tags__code=tag_query)
            
        return queryset