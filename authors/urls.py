from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    # * Register
    path("register/", views.register_view, name='register'),
    path("register/create/", views.register_create, name='register_create'),
    # * Login & Logout
    path("login/", views.login_view, name='login'),
    path("login/create/", views.login_create, name='login_create'),
    path("login/logout_view/", views.logout_view, name='logout_view'),
    # * Dashboard
    path("dashboard/", views.dashboard, name='dashboard'),
    path(
        "dashboard/recipe/",
        views.dashboard_recipe_view,
        name='dashboard_recipe_view'
    ),
    path(
        "dashboard/recipe/create/",
        views.dashboard_recipe_create,
        name='dashboard_recipe_create'
    ),
    path(
        "dashboard/recipe/<int:id>/edit/",
        # views.DashboardRecipe.as_view(),
        views.dashboard_recipe_edit,
        name='dashboard_recipe_edit'
    ),
    path(
        "dashboard/recipe/delete/",
        views.dashboard_recipe_delete,
        name='dashboard_recipe_delete'
    ),
]