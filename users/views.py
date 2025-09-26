from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from shop import models

def register(request):
    category = models.Category.objects.all()
    contact = models.Concacts.objects.all()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'category': category, 'contact':contact })


@login_required
def profile(request):
    category = models.Category.objects.all()
    contact = models.Concacts.objects.all()
    return render(request, 'users/profile.html', {'category': category, 'contact':contact})

def login(request):
    category = models.Category.objects.all()
    contact = models.Concacts.objects.all()
    return render(request, 'users/login.html', {'category': category, 'contact':contact})

