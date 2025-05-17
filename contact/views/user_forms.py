from django.shortcuts import render, redirect
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

def register(request):
    """
    Handles the user registration process.

    This view allows a new user to fill out a registration form.
    If the form submission is valid, the user is created and redirected to the login page.

    Args:
        request (HttpRequest): The request object containing user data.

    Returns:
        HttpResponseRedirect: Redirects to the login page after successful registration.
        HttpResponse: Renders the registration form if there are validation errors.
    """

    # Initialize an empty registration form
    form = RegisterForm()

    if request.method == 'POST': # Check if request method is POST
        form = RegisterForm(request.POST) # Populate the form with received data

        if form.is_valid(): # Validate the form
            form.save()  # Save the new user to the database
            messages.success(request, 'Usuario registrado') # Display success message
            return redirect('contact:login')  # Redirect to login page

    # Render the registration form (empty or with validation errors)
    return render(
        request,
        'contact/register.html',
        {
            'form': form
        }
    )


def login_view(request):
    """
    Handles user authentication.

    This view presents a login form where users provide their credentials. 
    If authentication is successful, the user is logged in and redirected to the index page.
    Otherwise, an error message is displayed.

    Args:
        request (HttpRequest): The request object containing login credentials.

    Returns:
        HttpResponseRedirect: Redirects to the index page upon successful login.
        HttpResponse: Renders the login page with validation errors if authentication fails.
    """

    # Initialize the authentication form
    form = AuthenticationForm(request)
    
    if request.method == 'POST': # Check if the request method is POST
        form = AuthenticationForm(request, data=request.POST) # Populate form with POST data

        if form.is_valid(): # Validate login credentials
            user = form.get_user() # Retrieve authenticated user
            auth.login(request, user) # Log in the user
            messages.success(request, 'Logado com sucesso!') # Success message
            return redirect('contact:index') # Redirect to main page
        else:
            messages.error(request, 'Login inválido') # Display error message

    # Render login page (empty or with validation errors)
    return render(request,
            'contact/login.html',
        {
            'form': form
        }
    )

@login_required(login_url='contact:login')
def user_update(request):
    """
    Handles updating user information.

    This view allows an authenticated user to update their personal details.
    If the request method is POST and the form is valid, the changes are saved.

    Args:
        request (HttpRequest): The request object containing user data.

    Returns:
        HttpResponseRedirect: Redirects to the user update page upon successful update.
        HttpResponse: Renders the registration update form if submission fails.
    """

    # Initialize form with current user data
    form = RegisterUpdateForm(instance=request.user)

    if request.method != "POST": # If request is not POST, render the form
        return render(
            request,
            'contact/register.html',
            {
                'form': form
            }
        )

    form = RegisterUpdateForm(data=request.POST, instance=request.user)   # Populate form with submitted data
    
    if not form.is_valid(): # Validate form and check errors
        return render(
            request,
            'contact/register.html',
            {
                'form': form
            }
        )
    
    form.save()   # Save updated user information
    return redirect('contact:user_update')  # Redirect to the user update page

@login_required(login_url='contact:login')
def logout_view(request):
    """
    Handles user logout.

    This view logs out the current authenticated user and redirects them to the login page.

    Args:
        request (HttpRequest): The request object containing user session data.

    Returns:
        HttpResponseRedirect: Redirects to the login page after logout.
    """
    auth.logout(request) # Log out the current user
    return redirect("contact:login") # Redirect to the login page

