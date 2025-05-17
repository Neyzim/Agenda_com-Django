from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation



class ContactForm(forms.ModelForm):
    """
    Form for creating and updating contact information.

    Includes an optional profile picture and category selection.
    Validates that certain fields are properly formatted.

    Fields:
        - first_name (str): First name of the contact.
        - last_name (str): Last name of the contact.
        - phone (str): Contact phone number.
        - email (EmailField): Contact email address.
        - description (str): Additional information about the contact.
        - category (ForeignKey): Category associated with the contact.
        - picture (ImageField): Optional profile picture.

    Methods:
        - clean_first_name(): Validates that 'ABC' is not used as a first name.
    """

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ), required=False
    )

    class Meta:
        model = models.Contact
        fields = (
                'first_name',
                'last_name',
                'phone',
                'email',
                'description',
                'category',
                'picture',
                )
     
    def clean(self):
         """Calls the parent clean method to ensure validation."""
         return super().clean()
    
    def clean_first_name(self):
        """Validates that 'ABC' is not used as a first name."""
        first_name = self.cleaned_data.get('first_name')
        if first_name == "ABC":
            self.add_error(
                'first_name',
                ValidationError("Não digite ABC idiota",
                code="invalid",
                )
            )
        return first_name


class RegisterForm(UserCreationForm):
    """
    Handles user registration with additional validation.

    This form extends Django's built-in `UserCreationForm` to include email validation.

    Fields:
        - first_name (str): Required, minimum length of 3 characters.
        - last_name (str): Required, minimum length of 3 characters.
        - email (EmailField): Required, must be unique.
        - username (str): Required.
        - password1 (str): Required, first password field.
        - password2 (str): Required, second password field (confirmation).

    Methods:
        - clean_email(): Ensures email uniqueness in the database.
    """
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
    )

    email = forms.EmailField(
        required=True
    )
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )

    def clean_email(self):
        """Checks if the email is already registered."""
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error('email',
                ValidationError('Já existe um email cadastrado igual a este!',code='invalid')
            )
            
        return email
    

class RegisterUpdateForm(forms.ModelForm):
    """
    Handles user profile updates, including password changes.

    This form allows users to update their personal information and set a new password if desired.

    Fields:
        - first_name (str): Required, minimum length of 2 characters.
        - last_name (str): Required, minimum length of 2 characters.
        - email (EmailField): Required, must be unique.
        - username (str): Required.
        - password1 (str): Optional, new password field.
        - password2 (str): Optional, confirmation of new password.

    Methods:
        - clean(): Validates that both password fields match.
        - save(): Saves user data, updating password if provided.
        - clean_email(): Ensures email uniqueness upon update.
        - clean_password1(): Validates new password against Django's password policies.
    """
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )

        def clean(self):
            """Ensures that both passwords match if provided."""
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if password1 or password2:
                if password1 != password2:
                    self.add_error(
                        'password2',
                        ValidationError('Senhas não batem')
                    )

            return super().clean()
            
        def save(self, commit=True):
            """Saves the user data, updating the password if provided."""
            cleaned_data = self.cleaned_data
            user = super().save(commit=False)
            password = cleaned_data.get('password1')

            if password:
                user.set_password(password)

            if commit:
                user.save()

            return user

        def clean_email(self):
            """Ensures email uniqueness when updating."""
            email = self.cleaned_data.get('email')
            current_email = self.instance.email

            if current_email != email:
                if User.objects.filter(email=email).exists():
                    self.add_error(
                        'email',
                        ValidationError('Já existe este e-mail', code='invalid')
                    )

            return email
        


        def clean_password1(self):
            """Validates new password using Django's built-in policies."""
            password1 = self.cleaned_data.get('password1')

            if password1:
                try:
                    password_validation.validate_password(password1)
                except ValidationError as errors:
                    self.add_error(
                        'password1',
                        ValidationError(errors)
                    )

            return password1