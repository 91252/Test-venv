from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Хранилище для истории (простая замена базе данных)
history_storage = []

@csrf_exempt
def calculator_view(request):
    result = None
    error = None
    num1 = ''
    num2 = ''
    operation = '+'
    
    if request.method == 'POST':
        try:
            num1 = request.POST.get('num1', '')
            num2 = request.POST.get('num2', '')
            operation = request.POST.get('operation', '+')
            
            # Преобразуем в числа
            a = float(num1)
            b = float(num2)
            
            # Вычисляем
            if operation == '+':
                result = a + b
            elif operation == '-':
                result = a - b
            elif operation == '*':
                result = a * b
            elif operation == '/':
                if b != 0:
                    result = a / b
                else:
                    error = "❌ Ошибка: Деление на ноль!"
            
            # Сохраняем в историю, если нет ошибки
            if result is not None and error is None:
                history_storage.insert(0, {
                    'num1': a,
                    'num2': b,
                    'operation': operation,
                    'result': result
                })
                # Оставляем только последние 5 записей
                if len(history_storage) > 5:
                    history_storage.pop()
                    
        except ValueError:
            error = "❌ Ошибка: Пожалуйста, введите корректные числа!"

    # Формируем HTML-код для блока истории
    history_html = ''
    for item in history_storage:
        history_html += f'''
        <div class="history-item">
            {item["num1"]} {item["operation"]} {item["num2"]} = <strong>{item["result"]}</strong>
        </div>
        '''
    
    if not history_html:
        history_html = '<div class="history-empty">История пока пуста</div>'

    # Формируем HTML-код для результата
    result_html = ''
    if result is not None:
        result_html = f'<div class="result-box">✅ Результат: <span class="result-number">{result}</span></div>'
    if error:
        result_html = f'<div class="error-box">{error}</div>'

    # HTML-верстка страницы
    full_html = f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Калькулятор с историей</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            .app-container {{
                display: flex;
                gap: 30px;
                flex-wrap: wrap;
                justify-content: center;
                max-width: 800px;
                margin: 0 auto;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 24px;
                padding: 30px;
                box-shadow: 0 25px 45px rgba(0,0,0,0.2);
                backdrop-filter: blur(10px);
                width: 340px;
                transition: transform 0.2s;
            }}
            .card:hover {{
                transform: translateY(-5px);
            }}
            h1, h2 {{
                text-align: center;
                color: #333;
                margin-bottom: 25px;
                font-weight: 600;
            }}
            h1 {{ font-size: 1.8rem; }}
            h2 {{ font-size: 1.4rem; border-bottom: 2px solid #667eea; display: inline-block; padding-bottom: 5px; margin-bottom: 20px; width: auto; }}
            .input-group {{
                margin-bottom: 20px;
            }}
            label {{
                display: block;
                margin-bottom: 8px;
                color: #555;
                font-weight: 500;
                font-size: 0.9rem;
            }}
            input, select {{
                width: 100%;
                padding: 12px;
                font-size: 1rem;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                transition: all 0.3s;
                background: #f8f9fa;
            }}
            input:focus, select:focus {{
                outline: none;
                border-color: #667eea;
                background: white;
            }}
            button {{
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 1.1rem;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                margin-top: 10px;
            }}
            button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(40,167,69,0.3);
            }}
            .result-box {{
                margin-top: 25px;
                padding: 15px;
                background: #e8f5e9;
                border-radius: 16px;
                text-align: center;
                font-size: 1.2rem;
                font-weight: bold;
                color: #2e7d32;
                border-left: 4px solid #28a745;
            }}
            .result-number {{
                font-size: 1.6rem;
                color: #1b5e20;
                margin-left: 10px;
            }}
            .error-box {{
                margin-top: 25px;
                padding: 15px;
                background: #ffebee;
                border-radius: 16px;
                text-align: center;
                font-weight: bold;
                color: #c62828;
                border-left: 4px solid #dc3545;
            }}
            .history-item {{
                background: #f8f9fa;
                padding: 12px;
                margin-bottom: 12px;
                border-radius: 12px;
                font-family: monospace;
                font-size: 1rem;
                border-left: 3px solid #667eea;
                transition: background 0.2s;
            }}
            .history-item:hover {{
                background: #e9ecef;
            }}
            .history-empty {{
                text-align: center;
                color: #adb5bd;
                padding: 30px;
                font-style: italic;
            }}
            .history-scroll {{
                max-height: 350px;
                overflow-y: auto;
                padding-right: 5px;
            }}
            .operator-select {{
                font-weight: bold;
            }}
            footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 0.7rem;
                color: #aaa;
            }}
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="card">
                <h1>🧮 Калькулятор</h1>
                <form method="POST">
                    <div class="input-group">
                        <label>📌 Первое число</label>
                        <input type="number" name="num1" step="any" value="{num1}" placeholder="Введите число" required>
                    </div>
                    <div class="input-group">
                        <label>⚙️ Операция</label>
                        <select name="operation" class="operator-select">
                            <option value="+" {'selected' if operation == '+' else ''}>➕ Сложение (+)</option>
                            <option value="-" {'selected' if operation == '-' else ''}>➖ Вычитание (-)</option>
                            <option value="*" {'selected' if operation == '*' else ''}>✖️ Умножение (*)</option>
                            <option value="/" {'selected' if operation == '/' else ''}>➗ Деление (/)</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label>📌 Второе число</label>
                        <input type="number" name="num2" step="any" value="{num2}" placeholder="Введите число" required>
                    </div>
                    <button type="submit">🚀 ПОСЧИТАТЬ</button>
                </form>
                {result_html}
                <footer>Работает с историей</footer>
            </div>
            <div class="card">
                <div style="text-align: center;">
                    <h2>📜 ИСТОРИЯ</h2>
                </div>
                <div class="history-scroll">
                    {history_html}
                </div>
                <footer>Последние 5 операций</footer>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return HttpResponse(full_html)

# Главные маршруты проекта
urlpatterns = [
    path('admin/', admin.site.urls),  # Админ-панель Django (по желанию)
    path('', calculator_view),        # Главная страница с калькулятором
]