from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # redirecione para a página inicial ou qualquer outra
        else:
            # Tratar erro de autenticação
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})
    return render(request, 'login/login.html')