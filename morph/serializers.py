from rest_framework import serializers
from .models import Tag, Morpheme

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['code', 'description', 'gloss']

class MorphemeSerializer(serializers.ModelSerializer):
   
    tags = TagSerializer(many=True, read_only=True)
    adds_tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Morpheme
        fields = ['id', 'surface', 'morph_type', 'underlying', 'tags', 'adds_tags']