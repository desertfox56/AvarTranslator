from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .proccesors import SimpleAvarAnalyzer

def index(request):
    """Главная страница с формой"""
    return render(request, 'analyzer/index.html')

def analyze_api(request):
    """API для анализа текста"""
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if not text:
            return JsonResponse({'error': 'Текст не предоставлен'}, status=400)
        
        analyzer = SimpleAvarAnalyzer()
        try:
            result = analyzer.analyze_phrase(text)
            return JsonResponse({'result': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Только POST запросы'}, status=405)

def test_analysis(request):
    """Тестовая страница для проверки анализатора"""
    analyzer = SimpleAvarAnalyzer()
    
    # Тестовые фразы
    test_phrases = [
        'кIалса вачIана',
        'хва вачIана',
        'кIалса лъугьана',
    ]
    
    results = []
    for phrase in test_phrases:
        try:
            result = analyzer.analyze_phrase(phrase)
            results.append(result)
        except Exception as e:
            results.append({'phrase': phrase, 'error': str(e)})
    
    return HttpResponse(f"""
    <html>
    <head><title>Тест анализатора</title></head>
    <body>
        <h1>Тест лингвистического анализатора</h1>
        <h2>Протестированные фразы:</h2>
        <pre>{results}</pre>
        <h2>Сырой вывод анализатора:</h2>
        <pre>{results}</pre>
        <hr>
        <p><a href="/">На главную (с формой)</a></p>
    </body>
    </html>
    """)