from django.shortcuts import render, redirect
from django import forms

# Определяем форму
class MyForm(forms.Form):
    checkbox1 = forms.BooleanField(required=False, label="Чекбокс 1")
    checkbox2 = forms.BooleanField(required=False, label="Чекбокс 2")
    checkbox3 = forms.BooleanField(required=False, label="Чекбокс 3")


# Обработчик представления GET-запроса
def func_get(request):
    # Создаем инстанс формы
    form = MyForm()
    return render(request, 'base.html', {'form': form})

# Обработчик представления POST-запроса
def func_post(request):
    # Создаем инстанс формы
    form = MyForm(request.POST)

    # Проверяем, валидна ли форма
    if form.is_valid():
        # Обрабатываем данные формы
        selected_checkboxes = {
            'checkbox1': form.cleaned_data['checkbox1'],
            'checkbox2': form.cleaned_data['checkbox2'],
            'checkbox3': form.cleaned_data['checkbox3'],
        }
        # Здесь вы можете сделать что-то с данными, например, сохранить их в базе данных

        # Можно добавить сообщение об успехе или перенаправление
        return render(request, 'success.html', {'selected_checkboxes': selected_checkboxes})
    else:
        #Возвращаем форму с ошибками если валидация не прошла.
        return render(request, 'base.html', {'form': form})


