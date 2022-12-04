from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)
        
    def test_if_recipe_view_render_specific_recipe(self):
        self.make_recipe(title='My recipe')
        
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn('My recipe', content)        
        