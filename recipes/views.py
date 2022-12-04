from os import environ

from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(environ.get('PER_PAGE'))
QTY_PAGES = int(environ.get('QTY_PAGES'))

# Create your views here.
def home(request):
    recipes = Recipe.objects.all().filter(is_published=True).order_by('-id')
    
    page_obj, pagination_range = make_pagination(
        request=request,
        query_set=recipes,
        per_page=PER_PAGE,
        qty_pages=QTY_PAGES
    )
    
    # messages.error(request, 'ERRO')
    # messages.success(request, 'SUCESSO')
    # messages.info(request, 'INFO')
    # messages.debug(request, 'DEBUG')
    # messages.warning(request, 'WARN')
    
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })
    
def category(request, category_id):
    recipes = Recipe.objects.all().filter(
        category__id=category_id, 
        is_published=True
        ).order_by('-id')

    if not recipes:
        return HttpResponse(content="Not Found", status=404)
    
    page_obj, pagination_range = make_pagination(
        request=request,
        query_set=recipes,
        per_page=PER_PAGE,
        qty_pages=QTY_PAGES
    )
    
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': recipes.first().category.name
        # 'recipes': [make_recipe(i) for i in range(10)]
    })

def recipe(request, id):
    recipe = Recipe.objects.all().filter(
        id=id, 
        is_published=True
        ).order_by('-id').first()
    
    if not recipe:
        return HttpResponse(content="Not Found", status=404)
    
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })

def search(request):
    search_term = request.GET.get('q', '').strip()
    
    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(category__name__icontains=search_term)
        ),
        is_published=True
    ).order_by('-id')
    
    page_obj, pagination_range = make_pagination(
        request=request,
        query_set=recipes,
        per_page=PER_PAGE,
        qty_pages=QTY_PAGES
    )
    
    return render(request, 'recipes/pages/search.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'additional_url_query': f'&q={search_term}'
    })