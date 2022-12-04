from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from authors.forms import RecipeForm
from recipes.models import Recipe


class DashboardRecipe(View):
    def get_recipe(self, id):
        recipe = None
        
        if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id
            ).first()
            
            if not recipe:
                raise Http404()
    
    def get(self, request, id):
        recipe = self.get_recipe(id)
        
        form = RecipeForm(instance=recipe)

        
        return render(request, 'authors/pages/dashboard_recipe.html', {
            'recipe': recipe,
            'form': form
        })
    def post(self, request, id):
        self.request

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