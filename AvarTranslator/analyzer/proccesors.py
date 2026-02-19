from lexicon.models import Root, Affix

class SimpleAvarAnalyzer:
    def analyze_phrase(self, phrase):
        """Анализирует фразу типа 'кIалса вачIана'"""
        words = phrase.split()
        analysis = []
        
        for word in words:
            word_analysis = self.analyze_word(word)
            analysis.append(word_analysis)
        
        return {
            'phrase': phrase,
            'words': analysis,
            'translation': self.generate_translation(analysis)
        }
    
    def analyze_word(self, word):
        """Разбирает одно слово"""
        # Ищем корень
        root_match = None
        for root_obj in Root.objects.filter(language__code='avar'):
            if word.startswith(root_obj.root):
                root_match = root_obj
                break
        
        if not root_match:
            return {'word': word, 'error': 'Корень не найден'}
        
        # Отсекаем корень, остаток - аффиксы
        remaining = word[len(root_match.root):]
        affixes_found = []
        
        # Ищем аффиксы в оставшейся части
        for affix_obj in Affix.objects.filter(language__code='avar').order_by('-position'):
            if remaining.endswith(affix_obj.affix):
                affixes_found.append({
                    'affix': affix_obj.affix,
                    'value': affix_obj.grammatical_value,
                    #'category': affix_obj.grammatical_category
                })
                remaining = remaining[:-len(affix_obj.affix)]
        
        return {
            'word': word,
            'root': root_match.root,
            'root_gloss': root_match.gloss,
            'root_pos': root_match.pos,
            'affixes': affixes_found,
            'remaining': remaining  # Должно быть пустой строкой если все верно
        }
    
    def generate_translation(self, word_analyses):
        """Генерирует перевод на основе анализа"""
        translation_parts = []
        
        for analysis in word_analyses:
            if 'error' in analysis:
                translation_parts.append(f"[{analysis['word']}]")
            else:
                # Простая логика: корень + пояснения по аффиксам
                part = analysis['root_gloss']
                for affix in analysis['affixes']:
                    if affix['value'] == 'ERG':
                        part += ' (эргатив)'
                    elif affix['value'] == 'PAST':
                        part += ' (прош.вр.)'
                    elif affix['value'] == 'ABS':
                        part += ' (абсолютив)'
                translation_parts.append(part)
        
        return ' '.join(translation_parts)

# Использование
if __name__ == '__main__':
    analyzer = SimpleAvarAnalyzer()
    result = analyzer.analyze_phrase('кIалса вачIана')
    print(result)