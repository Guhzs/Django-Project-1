from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForm


# * LOGIN
def login_view(request):
    login_form_data = request.session.get('login_form_data', None)
    
    form = LoginForm(login_form_data)

    return render(request, 'authors/pages/login_new.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })
    
def login_create(request):
    if not request.POST:
        raise(Http404())
    
    POST = request.POST
    request.session['login_form_data'] = POST
    
    form = LoginForm(POST)
    login_url = reverse('authors:login')
    
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        
        if authenticated_user is not None:
            del(request.session['login_form_data'])
            
            messages.success(request, 'You are logged in.')
            login(request=request, user=authenticated_user)
            return redirect(reverse('authors:dashboard'))
        
        messages.error(request, 'Invalid credentials!')
        return redirect(login_url)
    
    messages.error(request, 'Error to validate form data!')
    return redirect(login_url)

# * LOGOUT
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    logout(request)
    
    return redirect(reverse('authors:login'))