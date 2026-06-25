import os
import re
import json
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avarTranslator.settings')
django.setup()

from morph.models import Tag, Morpheme, LexiconEntry

def parse_lexc(content):
    """Парсит содержимое .lexc и возвращает структуру"""
    lines = content.splitlines()
    result = {
        "multichar_symbols": [],
        "lexicons": {}
    }
    current_lexicon = None
    in_symbols = False
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith('!'):
            continue
        if line.startswith('Multichar_Symbols'):
            in_symbols = True
            continue
        if line.startswith('LEXICON'):
            parts = line.split()
            if len(parts) >= 2:
                current_lexicon = parts[1]
                result["lexicons"][current_lexicon] = []
                in_symbols = False
            continue
        if in_symbols:
            # Можно собрать теги, но пока пропустим
            continue
        if current_lexicon is not None and line.endswith(';'):
            rule = line[:-1].strip()
            if ':' in rule:
                left, right = rule.split(':', 1)
                parts = right.strip().split()
                output = parts[0] if parts else ''
                next_lex = parts[1] if len(parts) > 1 else '#'
                result["lexicons"][current_lexicon].append({
                    "input": left.strip(),
                    "output": output,
                    "next": next_lex
                })
    return result

def import_lexicon_data(json_data):
    # Сначала создадим теги из multichar_symbols (пока оставим пустым)
    # В реальности нужно извлечь теги из входных строк
    tag_cache = {}
    def get_or_create_tag(code):
        code_clean = code.replace('%<', '').replace('%>', '').strip()
        if code_clean not in tag_cache:
            tag, _ = Tag.objects.get_or_create(code=code_clean)
            tag_cache[code_clean] = tag
        return tag_cache[code_clean]

    for lexicon_name, entries in json_data['lexicons'].items():
        for entry in entries:
            input_str = entry['input']
            output_str = entry['output']
            next_lex = entry['next']
            # Извлечём теги из input_str (начинаются с %< и заканчиваются %>)
            tags_found = re.findall(r'%<([^%]+)%>', input_str)
            # Создадим морфему (пока не очень точно, но для прототипа сойдёт)
            # Определим тип: если вход содержит только теги без конкретной строки – это аффикс
            # Но мы упростим: создадим запись в LexiconEntry
            LexiconEntry.objects.create(
                lexicon_name=lexicon_name,
                input_pattern=input_str,
                output_pattern=output_str,
                next_lexicon=next_lex
            )

if __name__ == '__main__':
    # Укажите путь к вашему .txt файлу
    file_path = 'apertium-ava_ava.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parsed = parse_lexc(content)
    # Для отладки можно сохранить JSON
    with open('parsed_lexc.json', 'w', encoding='utf-8') as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)
    import_lexicon_data(parsed)
    print("Импорт завершён.")