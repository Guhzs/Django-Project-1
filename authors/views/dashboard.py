from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import RecipeForm
from recipes.models import Recipe


# * DASHBOARD
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    
    return render(request, 'authors/pages/dashboard.html', {
        'recipes': recipes
    })
    
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_view(request):
    dashboard_recipe_new_form_data = request.session.get('dashboard_recipe_new_form_data', None)
    
    form = RecipeForm(dashboard_recipe_new_form_data)

    return render(request, 'authors/pages/dashboard_recipe_new.html', {
        'form': form,
        'form_action': reverse('authors:dashboard_recipe_create')
    })
    
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    if not request.POST:
        raise(Http404())
    
    POST = request.POST
    
    request.session['dashboard_recipe_new_form_data'] = POST
    
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    

    if form.is_valid():
        recipe = form.save(commit=False)
        
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        
        recipe.save()
        
        messages.success(request, 'Your recipe has been successfully saved')
        
        del(request.session['dashboard_recipe_new_form_data'])
        
        return redirect(reverse('authors:dashboard'))
    
    return redirect('authors:dashboard_recipe_view')

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()
    
    if not recipe:
        raise Http404()
    
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    
    if form.is_valid():
        recipe = form.save(commit=False)
        
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        
        recipe.save()
        
        messages.success(request, 'Your recipe has been successfully saved')
        
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))
    
    return render(request, 'authors/pages/dashboard_recipe.html', {
        'recipe': recipe,
        'form': form
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise(Http404())
    
    POST = request.POST
    id = POST.get('id')
    
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()
    
    if not recipe:
        raise Http404()

    recipe.delete()
    messages.success(request, 'Delete Successfully!')
    return redirect(reverse('authors:dashboard'))
