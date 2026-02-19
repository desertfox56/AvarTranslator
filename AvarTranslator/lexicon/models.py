from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    """Модель для описания языка."""
    code = models.CharField(max_length=10, unique=True, verbose_name="Код (напр., avar)")
    name = models.CharField(max_length=100, verbose_name="Название")
    family = models.CharField(max_length=50, verbose_name="Семья")
    is_ergative = models.BooleanField(default=False, verbose_name="Эргативный строй")
    is_agglutinative = models.BooleanField(default=True, verbose_name="Агглютинативный")

    # Простые метаданные: когда создана/обновлена запись
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Root(models.Model):
    """Модель для корня (лексемы) слова."""
    POS_CHOICES = [('noun', 'Существительное'), ('verb', 'Глагол'), ('adj', 'Прилагательное')]

    # Основные лингвистические данные
    root = models.CharField(max_length=200, verbose_name="Корень")
    gloss = models.CharField(max_length=300, verbose_name="Основной перевод")
    pos = models.CharField(max_length=20, choices=POS_CHOICES, verbose_name="Часть речи")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Язык")
    noun_class = models.CharField(  # ЗАМЕНИЛИ gender на noun_class
        max_length=10,
        blank=True,
        verbose_name="Именной класс",
        help_text="Напр.: I (в-), II (й-), III (б-), IV (р-) для аварского"
    )

    # Простые, но полезные метаданные
    source = models.CharField(max_length=200, blank=True, verbose_name="Источник записи")
    verified = models.BooleanField(default=False, verbose_name="Проверено")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['root', 'language']  # Один корень на язык

    def __str__(self):
        return f"{self.root} ({self.gloss})"

class Affix(models.Model):
    """Модель для аффиксов (морфем)."""
    AFFIX_TYPES = [('suffix', 'Суффикс'), ('prefix', 'Префикс')]

    affix = models.CharField(max_length=50, verbose_name="Аффикс")
    affix_type = models.CharField(max_length=10, choices=AFFIX_TYPES, verbose_name="Тип")
    grammatical_value = models.CharField(max_length=50, verbose_name="Грамм. значение")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Язык")
    position = models.IntegerField(default=0, help_text="Порядок в слове (0 сразу после корня)")

    # Примеры использования
    examples = models.TextField(blank=True, verbose_name="Примеры")

    def __str__(self):
        return f"{self.affix} -> {self.grammatical_value}"