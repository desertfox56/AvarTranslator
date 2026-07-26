import os
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avarTranslator.settings')
django.setup()

from morph.models import Tag, Morpheme, LexiconEntry

# Улучшенные регулярные выражения (учитывают <tag> и %<tag%>)
TAG_PATTERN = re.compile(r'%<([^%]+)%>|<([^>]+)>')
ALTERNATION_PATTERN = re.compile(r'%\{([^}]+)\%\}')

def unescape_apertium(text):
    
    if not text: return text
    text = text.replace('%-', '-')
    text = text.replace('%+', '+')
    text = text.replace('%~', '~')
    text = text.replace('%#', '#')
    text = text.replace('%%', '%')
    text = text.replace('0', '') # 0 часто означает пустую строку (epsilon)
    return text

def parse_tags_and_text(pattern):
    tags = []
    text = pattern
    alternations = []
    
    # 1. Извлекаем теги
    for match in TAG_PATTERN.finditer(pattern):
        tag_code = match.group(1) or match.group(2)
        if tag_code:
            tags.append(tag_code)
        text = text.replace(match.group(0), '')
        
    # 2. Извлекаем чередования
    for match in ALTERNATION_PATTERN.finditer(pattern):
        alternations.append(match.group(1))
        text = text.replace(match.group(0), '')
        
    # 3. Снимаем экранирование с оставшегося текста
    text = unescape_apertium(text.strip())
    
    return tags, text, alternations

def normalize_all():
    tag_cache = {}
    def get_or_create_tag(code):
        if code not in tag_cache:
            tag, _ = Tag.objects.get_or_create(code=code)
            tag_cache[code] = tag
        return tag_cache[code]

    print("Начинаем нормализацию. Получение записей...")
    entries = LexiconEntry.objects.all()
    total = entries.count()
    processed = 0
    
    for entry in entries:
        processed += 1
        if processed % 1000 == 0:
            print(f'Обработано {processed} из {total}')
            
        in_tags, in_text, in_alts = parse_tags_and_text(entry.input_pattern)
        out_tags, out_text, out_alts = parse_tags_and_text(entry.output_pattern)

        # Обработка левой части (input) - обычно это корень/основа
        if in_text:
            tag_objs = [get_or_create_tag(t) for t in in_tags]
            morpheme, _ = Morpheme.objects.get_or_create(
                surface=in_text,
                defaults={
                    'morph_type': 'root', 
                    'underlying': in_text, 
                    'description': 'Из LEXC (input)'
                }
            )
            # Добавляем теги, если они новые
            if tag_objs:
                morpheme.tags.add(*tag_objs)
            
            entry.morpheme = morpheme
            entry.save()

        # Обработка правой части (output) - обычно это добавляемый аффикс
        if out_text and out_text != in_text:
            tag_objs = [get_or_create_tag(t) for t in out_tags]
            morpheme, _ = Morpheme.objects.get_or_create(
                surface=out_text,
                defaults={
                    'morph_type': 'suffix', 
                    'underlying': out_text, 
                    'description': 'Аффикс из LEXC (output)'
                }
            )
            if tag_objs:
                morpheme.adds_tags.add(*tag_objs)
            
            # Если запись LexiconEntry еще не связана с морфемой, свяжем
            if not entry.morpheme:
                entry.morpheme = morpheme
                entry.save()

    print('Нормализация завершена.')

if __name__ == '__main__':
    normalize_all()