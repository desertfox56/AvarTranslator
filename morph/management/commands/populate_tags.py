from django.core.management.base import BaseCommand
from morph.models import Tag

class Command(BaseCommand):
    help = 'Массовое заполнение описаний и глоссов для грамматических тегов'

    def handle(self, *args, **kwargs):
        # Это базовый словарь тегов
        
        tag_data = {
            'n': {'description': 'Существительное', 'gloss': 'N'},
            'vblex': {'description': 'Глагол', 'gloss': 'V'},
            'adv': {'description': 'Наречие', 'gloss': 'ADV'},
            'adj': {'description': 'Прилагательное', 'gloss': 'ADJ'},
            'num': {'description': 'Числительное', 'gloss': 'NUM'},
            'prn': {'description': 'Местоимение', 'gloss': 'PRN'},
            'post': {'description': 'Послелог', 'gloss': 'POST'},
            
            # Падежи
            'nom': {'description': 'Номинатив (Именительный)', 'gloss': 'NOM'},
            'erg': {'description': 'Эргатив', 'gloss': 'ERG'},
            'gen': {'description': 'Генетив (Родительный)', 'gloss': 'GEN'},
            'dat': {'description': 'Датив (Дательный)', 'gloss': 'DAT'},
            'loc': {'description': 'Локатив (Местный)', 'gloss': 'LOC'},
            
            # Число
            'sg': {'description': 'Единственное число', 'gloss': 'SG'},
            'pl': {'description': 'Множественное число', 'gloss': 'PL'},
            
            # Время и формы глагола
            'past': {'description': 'Прошедшее время', 'gloss': 'PST'},
            'pres': {'description': 'Настоящее время', 'gloss': 'PRS'},
            'fut': {'description': 'Будущее время', 'gloss': 'FUT'},
            'inf': {'description': 'Инфинитив', 'gloss': 'INF'},
            
            # Частицы и союзы 
            'emph': {'description': 'Усилительная частица', 'gloss': 'EMPH'},
            'mod': {'description': 'Модальная частица', 'gloss': 'MOD'},
            'qst': {'description': 'Вопросительная частица', 'gloss': 'QST'},
            'quot': {'description': 'Цитатная частица (квотатив)', 'gloss': 'QUOT'},
            'cnjcoo': {'description': 'Сочинительный союз', 'gloss': 'CONJ'},
        }

        updated_count = 0

        # Проходимся по словарю и обновляем базу
        for code, data in tag_data.items():
            # Ищем тег в базе данных по его коду
            tag = Tag.objects.filter(code=code).first()
            
            if tag:
                tag.description = data['description']
                tag.gloss = data['gloss']
                tag.save()
                
                # Выводим зеленое сообщение в консоль об успехе
                self.stdout.write(self.style.SUCCESS(f'Обновлен тег: {code} -> {data["gloss"]}'))
                updated_count += 1
            else:
                # Если тега из словаря нет в базе, просто предупреждаем
                self.stdout.write(self.style.WARNING(f'Тег не найден в базе (пропущен): {code}'))

        self.stdout.write(self.style.SUCCESS(f'\nГотово! Всего обновлено тегов: {updated_count}'))