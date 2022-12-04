from django.contrib import admin

from recipes.models import Category, Recipe


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    ...
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published',)
    list_display_links = ('title', 'created_at',)
    search_fields = ('id', 'title', 'description', 'slug', 'preparation_steps', 'created_at', 'category__name',)
    list_filter = ('category__name', 'author', 'is_published',)
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = ('-id',)
    prepopulated_fields = {
        "slug": ('title',)
    }

admin.site.register(Category, CategoryAdmin)

