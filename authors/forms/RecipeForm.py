from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._my_errors = defaultdict(list)
        
        add_attr(self.fields.get('preparation_steps'), 'parentClassName', 'col-md-12')
        add_attr(self.fields.get('cover'), 'parentClassName', 'col-md-12')
     
        add_attr(self.fields.get('preparation_steps'), 'class', 'form-control')
        add_attr(self.fields.get('cover'), 'class', 'form-control')
    
    preparation_time_unit = forms.CharField(
        required=True,
        widget=forms.Select(
            attrs={
            'class': 'form-control'
            },
            choices=(
                ('Minutos', 'Minutos'),
                ('Horas', 'Horas'),
            )
        ),
        label="Preparation Time Unit",
    )
    
    servings_unit = forms.CharField(
        required=True,
        widget=forms.Select(
            # attrs={
            # 'class': 'form-control'
            # },
            choices=(
                ('Porções', 'Porções'),
                ('Pedaços', 'Pedaços'),
                ('Pessoas', 'Pessoas'),
            )
        ),
        label="Servings Unit",
    )
    
    class Meta:
        model=Recipe
        fields= ('title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'category', 'preparation_steps', 'cover')
        
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        
        if len(title or '') < 5:
            self._my_errors['title'].append('Must have at least 5 chars')
            
        if title == description:
            self._my_errors['title'].append('Title and description cannot be equal')
            self._my_errors['description'].append('Title and description cannot be equal')
            
        if self._my_errors:
            raise ValidationError(self._my_errors)
        
        return super_clean