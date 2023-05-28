from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():  # если форма валидная
            username = request.POST['username']  # по ключу достаем из словаря логин и пароль
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)  # проверка аутентификации
            if user:  # если аутентификация успешна
                auth.login(request, user)  # авторизуем пользователя
                return HttpResponseRedirect(reverse('index'))  # перенаправляем на главную страницу
    else:  # если запрос - GET
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context=context)  # возвращаем страницу с авторизацией


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm
    context = {'form': form}
    return render(request, 'users/registration.html', context=context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        # instance=request.user - указываем чтобы для этого пользователя обновилась информация
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Store - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
