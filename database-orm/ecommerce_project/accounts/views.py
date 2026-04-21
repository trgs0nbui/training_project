from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from .forms import RegisterForm

# register logic
def register_view(request):
    form = RegisterForm()
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            login(request, user)
            
            return redirect('product_list')
        
    return render(request, 'accounts/register.html', {
        'form': form
    })
    
# login logic
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('product_list')
        
        return render(request, 'accounts/login.html', {
            'error': 'Invalid credentials'
        })
    
    return render(request, 'accounts/login.html')

# logout
def logout_view(request):
    logout(request)
    return redirect('login')