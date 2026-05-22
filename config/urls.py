from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

history = []

@csrf_exempt
def calculator_view(request):
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1', 0))
            num2 = float(request.POST.get('num2', 0))
            operation = request.POST.get('operation', '+')
            
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 != 0:
                    result = num1 / num2
                else:
                    error = "Ошибка: Деление на ноль!"
            
            if result is not None and not error:
                # Сохраняем в историю с датой
                history.append({
                    'num1': num1,
                    'num2': num2,
                    'operation': operation,
                    'result': result,
                    'created_at': datetime.now()
                })
                # Оставляем только последние 5 записей
                if len(history) > 5:
                    history.pop(0)
                    
        except ValueError:
            error = "Ошибка: Введите корректные числа!"
        except Exception as e:
            error = f"Ошибка: {str(e)}"
    
    context = {
        'result': result,
        'error': error,
        'history': history,
        'num1': request.POST.get('num1', ''),
        'num2': request.POST.get('num2', ''),
        'operation': request.POST.get('operation', '+'),
    }
    
    return render(request, 'calculator.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', calculator_view),
]