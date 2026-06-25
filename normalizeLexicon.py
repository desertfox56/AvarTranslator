import os
import sys
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avarTranslator.settings')
django.setup()

from morph.models import Tag, Morpheme, LexiconEntry

# Регулярка для извлечения тегов
TAG_PATTERN = re.compile(r'%<([^%]+)%>')
ALTERNATION_PATTERN = re.compile(r'%\{([^}]+)\%\}')

def parse_tags_and_text(pattern):
    """
    Разбирает строку типа '%<n%>%<m%>вас' на список тегов и оставшийся текст.
    Возвращает (tags, text_without_tags, alternations).
    """
    tags = []
    text = pattern
    alternations = []
    # Ищем теги
    for match in TAG_PATTERN.finditer(pattern):
        tag_code = match.group(1)
        tags.append(tag_code)
        # Удаляем тег из текста (заменяем на пустую строку)
        text = text.replace(match.group(0), '')
    # Ищем чередования (%{a%})
    for match in ALTERNATION_PATTERN.finditer(pattern):
        alt = match.group(1)
        alternations.append(alt)
        # Можно оставить как есть или заменить на реальный символ – пока оставим
    # Убираем служебные символы %>, %<, %{ и %}
    text = text.replace('%<', '').replace('%>', '').replace('%{', '').replace('%}', '')
    return tags, text.strip(), alternations

def normalize_all():
    # Сначала создадим все теги, которые встречаются
    tag_cache = {}
    def get_or_create_tag(code):
        if code not in tag_cache:
            tag, _ = Tag.objects.get_or_create(code=code)
            tag_cache[code] = tag
        return tag_cache[code]

    # Пройдём по всем записям
    total = LexiconEntry.objects.count()
    processed = 0
    for entry in LexiconEntry.objects.all():
        processed += 1
        if processed % 1000 == 0:
            print(f'Обработано {processed} из {total}')
        # Разбираем входную строку
        in_tags, in_text, in_alts = parse_tags_and_text(entry.input_pattern)
        # Разбираем выходную строку
        out_tags, out_text, out_alts = parse_tags_and_text(entry.output_pattern)

        # Определяем, является ли это правило аффиксом или корнем (по наличию текста)
        # Если in_text и out_text оба пусты – это чисто грамматическое правило (например, переход без добавления)
        # Если in_text непустой – это может быть корень или основа
        # Если out_text непустой – это добавляемый аффикс
        # Для простоты создадим морфему для каждого уникального текста с тегами

        # Создаём или получаем морфему для in_text (это может быть корень)
        if in_text:
            # Объединяем теги для морфемы (теги из входной строки)
            tag_objs = [get_or_create_tag(t) for t in in_tags]
            morpheme, _ = Morpheme.objects.get_or_create(
                surface=in_text,
                morph_type='root',  # пока считаем корнем, но позже можно уточнить
                defaults={'underlying': in_text, 'description': 'Из LEXC'}
            )
            morpheme.tags.set(tag_objs)
            morpheme.save()
            entry.morpheme = morpheme
            entry.save()

        # Если out_text непустой – это аффикс (или окончание)
        if out_text:
            tag_objs = [get_or_create_tag(t) for t in out_tags]
            # Определяем тип: если в out_text есть символы типа 'лъ', 'с' и т.п. – это суффикс
            # Пока считаем всё suffix
            morpheme, _ = Morpheme.objects.get_or_create(
                surface=out_text,
                morph_type='suffix',
                defaults={'underlying': out_text, 'description': 'Аффикс из LEXC'}
            )
            morpheme.tags.set(tag_objs)
            # Запоминаем, какие теги добавляет этот аффикс (теги из выходной строки)
            # Для этого используем adds_tags – добавим их
            for t in tag_objs:
                morpheme.adds_tags.add(t)
            morpheme.save()
            # Свяжем с entry, если ещё не связан
            if not entry.morpheme:
                entry.morpheme = morpheme
                entry.save()

        # Если есть чередования – сохраним их как отдельные Morpheme типа 'alternation'
        for alt in in_alts + out_alts:
            alt_morph, _ = Morpheme.objects.get_or_create(
                surface=alt,
                morph_type='alternation',
                defaults={'underlying': alt, 'description': f'Чередование {alt}'}
            )
            
    print('Нормализация завершена.')

if __name__ == '__main__':
    normalize_all()