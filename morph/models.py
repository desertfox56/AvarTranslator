from django.db import models

class Tag(models.Model):
    """Грамматический тег (например, 'n', 'm', 'erg', 'sg')"""
    code = models.CharField(max_length=20, unique=True)  
    description = models.TextField(blank=True)
    gloss = models.CharField(max_length=10,blank=True)
    # ERG, NOM, GEN, DAT, LOC, ALL, ABL, SG, PL, M, F, NT...

    def __str__(self):
        return self.code

class Morpheme(models.Model):
    TYPE_CHOICES = [
        ('root', 'Корень'),
        ('prefix', 'Префикс'),
        ('suffix', 'Суффикс'),
        ('infix', 'Инфикс'),
        ('ending', 'Окончание'),
        ('alternation', 'Фонетическое чередование'),
    ]
    morph_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    surface = models.CharField(max_length=50)          # как пишется в тексте
    underlying = models.CharField(max_length=50, blank=True)  # с чередованиями, если есть
    tags = models.ManyToManyField(Tag, blank=True)      # какие теги несёт эта морфема
    description = models.TextField(blank=True)
    # Для аффиксов – что добавляют
    adds_tags = models.ManyToManyField(Tag, related_name='added_by', blank=True)
    # Правило замены для чередований (например, %{a%} -> а, и т.п.)
    alternation_rule = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.surface

class LexiconEntry(models.Model):
    """Запись из LEXICON: вход -> выход -> следующий лексикон"""
    lexicon_name = models.CharField(max_length=100)
    input_pattern = models.CharField(max_length=200)   # что слева от :
    output_pattern = models.CharField(max_length=200)  # что справа от :
    next_lexicon = models.CharField(max_length=100, blank=True)
    # Привязка к морфемам 
    morpheme = models.ForeignKey(Morpheme, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.lexicon_name}: {self.input_pattern} -> {self.output_pattern}"