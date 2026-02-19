class MockAvarAnalyzer:
    """Простой анализатор-заглушка"""
    
    LEXICON = {
        "кIал": {"gloss": "мальчик", "pos": "NOUN"},
        "вачI": {"gloss": "прийти", "pos": "VERB"},
        "хва": {"gloss": "девочка", "pos": "NOUN"},
    }
    
    AFFIXES = {
        "са": {"type": "case", "value": "ERG"},
        "а": {"type": "case", "value": "ABS"},
        "на": {"type": "tense", "value": "PAST"},
        "би": {"type": "number", "value": "PL"},
    }
    
    def analyze(self, text):
        """Простой анализ (эвристический)"""
        words = text.split()
        results = []
        
        for word in words:
            analysis = self._analyze_word(word)
            results.append({
                "word": word,
                "analysis": analysis,
                "translation": self._get_translation(word)
            })
        
        return {
            "original": text,
            "words": results,
            "language": "avar",
            "status": "success"
        }
    
    def _analyze_word(self, word):
        """Эвристический разбор"""
        # Простейшие правила
        if word.endswith("са"):
            return {"root": word[:-2], "case": "erg"}
        elif word.endswith("на"):
            return {"root": word[:-2], "tense": "past"}
        elif word.endswith("би"):
            return {"root": word[:-2], "number": "plural"}
        else:
            return {"root": word, "note": "неизвестная форма"}
    
    def _get_translation(self, word):
        """Простой перевод"""
        for root, data in self.LEXICON.items():
            if word.startswith(root):
                return data["gloss"]
        return "неизвестно"