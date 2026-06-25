from django.contrib import admin
from .models import Tag, Morpheme, LexiconEntry

admin.site.register(Tag)
admin.site.register(Morpheme)
admin.site.register(LexiconEntry)