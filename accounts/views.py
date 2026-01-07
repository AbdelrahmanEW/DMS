"""
Authentication views
"""
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    """
    صفحة تسجيل الدخول
    """
    if request.user.is_authenticated:
        return redirect('documents:list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'مرحباً {user.get_full_name() or user.username}')
            
            # Redirect to next or default
            next_url = request.GET.get('next', 'documents:list')
            return redirect(next_url)
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    تسجيل الخروج
    """
    logout(request)
    messages.info(request, 'تم تسجيل الخروج بنجاح')
    return redirect('accounts:login')