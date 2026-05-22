from django.shortcuts import render

from .models import CalculationHistory


def index(request):
    result = None
    error = None

    if request.method == 'POST':
        try:
            # Получаем данные из формы
            num1 = float(request.POST.get('num1'))
            num2 = float(request.POST.get('num2'))
            operation = request.POST.get('operation')

            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    error = "На ноль делить нельзя!"
                else:
                    result = num1 / num2
            if error is None:
                CalculationHistory.objects.create(
                    num1=num1,
                    num2=num2,
                    operation=operation,
                    result=result
                )
        except (ValueError, TypeError):
            error = "Введите корректные числа"

    history = CalculationHistory.objects.order_by('-created_at')[:5]

    return render(request, 'calculator/index.html', {
        'result': result,
        'error': error,
        'history': history # передаем историю в шаблон
    })
    
    from django.shortcuts import render

def index(request):
    return render(request, 'calculator/index.html')