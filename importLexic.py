import os
import re
import json
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avarTranslator.settings')
django.setup()

from morph.models import Tag, Morpheme, LexiconEntry

def parse_lexc(content):
    lines = content.splitlines()
    result = {"lexicons": {}}
    current_lexicon = None
    
    for raw_line in lines:
        line = raw_line.strip()
        # Пропускаем пустые строки, комментарии (!) и заголовки символов
        if not line or line.startswith('!') or line.startswith('Multichar_Symbols'):
            continue
            
        if line.startswith('LEXICON'):
            parts = line.split()
            if len(parts) >= 2:
                current_lexicon = parts[1]
                result["lexicons"][current_lexicon] = []
            continue
            
        # Парсим строки вида: input:output next_lexicon ;
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
            else:
                # Правила без двоеточия: input_and_output next_lexicon ;
                parts = rule.split()
                val = parts[0] if parts else ''
                next_lex = parts[1] if len(parts) > 1 else '#'
                result["lexicons"][current_lexicon].append({
                    "input": val,
                    "output": val, # Если двоеточия нет, вход равен выходу
                    "next": next_lex
                })
    return result

def import_lexicon_data(json_data):
    print("Очистка старых данных LexiconEntry...")
    LexiconEntry.objects.all().delete()
    
    entries_to_create = []
    for lexicon_name, entries in json_data['lexicons'].items():
        for entry in entries:
            entries_to_create.append(LexiconEntry(
                lexicon_name=lexicon_name,
                input_pattern=entry['input'],
                output_pattern=entry['output'],
                next_lexicon=entry['next']
            ))
            
    print(f"Пакетное сохранение {len(entries_to_create)} записей...")
    LexiconEntry.objects.bulk_create(entries_to_create, batch_size=5000)

if __name__ == '__main__':
    # Путь к файлу словаря (убедись, что он правильный)
    file_path = 'apertium-ava_ava.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parsed = parse_lexc(content)
    import_lexicon_data(parsed)
    print("Импорт завершён.")