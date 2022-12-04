from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ? Another way to define values
        # add_placeholder(self.fields['username'], 'Your username')
        # add_placeholder(self.fields['email'], 'Your e-mail')
        # add_placeholder(self.fields['first_name'], 'Ex.: John')
        # add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: John',
            'class': 'form-control'
        }),
        label="Name",
        error_messages={'required': 'This field is required!'},
        help_text=""
    )
    
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Doe',
            'class': 'form-control'
        }),
        label="Last Name",
        error_messages={},
        help_text=""
    )
    
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your username here...',
            'class': 'form-control'
        }),
        label="Username",
        error_messages={
            'required': 'This field is required!',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters'
            },
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        min_length=4,
        max_length=150
    )
    
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Type your email here...',
            'class': 'form-control'
        }),
        label="E-mail",
        error_messages={'required': 'This field is required!'},
        help_text='The e-mail must be valid.'
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password here...',
            'class': 'form-control'
        }),
        label="Password",
        error_messages={'required': 'This field is required!'},
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password]
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
            'class': 'form-control'
        }),
        label="Confirm Your Password",
        error_messages={'required': 'Please, repeat your password'},
        help_text=""
    )
        
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username',
            'email',
            'password'
        ]
        
        # ? Case you want to render everything except a list of fields
        # exclude = ['first_name']
        
        # ? Another way to define everything
        # labels = {
        #     'first_name': 'Nome',
        #     'last_name': 'Sobrenome'
        # }
        
        # help_texts = {
        #     'first_name': 'Digite o primeiro nome',
        # }
        
        # error_messages = {
        #     'password': {
        #         'required': 'Required'
        #     }
        # }
        
        # widgets = {
        #     'first_name': forms.TextInput(attrs={
        #             'placeholder': 'Type your name...'
        #             'class': 'form-control'
        #         }), 
        #     'last_name': forms.TextInput(attrs={
        #             'placeholder': 'Type your surname...'
        #             'class': 'form-control'
        #         }), 
        #     'username': forms.TextInput(attrs={
        #             'placeholder': 'Type your username...'
        #             'class': 'form-control'
        #         }), 
        #     'email': forms.TextInput(attrs={
        #             'placeholder': 'Type your email...'
        #             'class': 'form-control'
        #         }), 
        #     'password': forms.TextInput(attrs={
        #             'placeholder': 'Type your password...'
        #             'class': 'form-control'
        #         }), 
        # }
        
    # ? Clean function for specific field
    # def clean_password(self):
    #     data = self.cleaned_data.get('password')
        
    #     if 'atenção' in data:
    #         raise ValidationError(
    #             'Não digite %(value)s no campo password',
    #             code='invalid',
    #             params={'value': 'atenção'}
    #         )
        
    #     return data
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        
        if exists:
            raise ValidationError('User e-mail is already in use', code='invalid')
        
        return email
    
    # ? Clean function for all fields
    def clean(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            raise ValidationError({
                'password': 'Password and Confirm Password Must Be The Same!',
                'password2': 'Password and Confirm Password Must Be The Same!',
            })
