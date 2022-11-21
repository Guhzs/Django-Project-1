from django.http import HttpResponse
from django.shortcuts import render

from recipes.models import Recipe


# Create your views here.
def home(request):
    recipes = Recipe.objects.all().filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes
        # 'recipes': [make_recipe(i) for i in range(10)]
    })
    
def category(request, category_id):
    recipes = Recipe.objects.all().filter(
        category__id=category_id, 
        is_published=True
        ).order_by('-id')
    
    if not recipes:
        return HttpResponse(content="Not Found", status=404)
    
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
        'title': recipes.first().category.name
        # 'recipes': [make_recipe(i) for i in range(10)]
    })

def recipe(request, id):
    recipe = Recipe.objects.all().filter(
        id=id, 
        is_published=True
        ).order_by('-id').first()
    
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True
    })
