# lexicon/admin.py

from django.contrib import admin
from .models import Language, Root, Affix

# 1. Настройка отображения модели Language в админке
class LanguageAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке записей
    list_display = ('code', 'name', 'family', 'is_ergative', 'is_agglutinative', 'created_at')
    # Поля, по которым можно искать записи
    search_fields = ('code', 'name', 'family')
    # Фильтры справа от списка
    list_filter = ('is_ergative', 'is_agglutinative', 'family')
    # Порядок сортировки (по умолчанию)
    ordering = ('code',)

# 2. Настройка отображения модели Root
class RootAdmin(admin.ModelAdmin):
    list_display = ('root', 'gloss', 'pos', 'language', 'noun_class', 'verified', 'created_at')
    search_fields = ('root', 'gloss', 'pos')
    list_filter = ('pos', 'language', 'verified', 'noun_class')
    ordering = ('root',)
    # Поля, которые можно редактировать прямо в списке (удобно для verified)
    list_editable = ('verified',)
    # Группировка полей на странице редактирования
    fieldsets = (
        (None, {
            'fields': ('root', 'gloss', 'pos', 'language', 'noun_class')
        }),
        ('Метаданные', {
            'fields': ('source', 'verified', 'created_by'),
            'classes': ('collapse',)  # Сворачиваемый блок
        }),
    )

# 3. Настройка отображения модели Affix
class AffixAdmin(admin.ModelAdmin):
    list_display = ('affix', 'affix_type', 'grammatical_value', 'language', 'position')
    search_fields = ('affix', 'grammatical_value')
    list_filter = ('affix_type', 'language', 'position')
    ordering = ('language', 'position', 'affix')

# 4. Регистрация моделей с их настройками
admin.site.register(Language, LanguageAdmin)
admin.site.register(Root, RootAdmin)
admin.site.register(Affix, AffixAdmin)