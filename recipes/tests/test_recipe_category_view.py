from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_category_is_paginated(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
            recipes = response.context['recipes']
            paginator = recipes.paginator
            
            self.assertEqual(paginator.num_pages, 1)
            self.assertEqual(len(paginator.get_page(1)), 1)
            # self.assertEqual(len(paginator.get_page(2)), 3)
            # self.assertEqual(len(paginator.get_page(3)), 2)
