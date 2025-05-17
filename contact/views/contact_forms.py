from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import Contact

# View for creating a contact:
@login_required(login_url='contact:login') #Restricts access to authenticated users. Redirects to the login page if not logged in.
def create(request):
    """
    Handle the creation of a new contact.

    This view allows an authenticated user to submit a form for creating a new contact. 
    If the form is valid, the contact is linked to the current user, saved in the database, 
    and the user is redirected to the contact update page. If the form is invalid, 
    the contact creation form is re-rendered with error messages.
    
    Args:
        request (HttpRequest): The request object containing user data.

    Returns:
        HttpResponseRedirect: Redirects to the contact update page if creation is successful.
        HttpResponse: Renders the contact creation form with errors if submission fails.
    
    """

    # Define the URL for form submission.
    form_action = reverse('contact:create') 

    
    if request.method == 'POST': #Check if the request method received is POST.
        form = ContactForm( 
            request.POST, 
            request.FILES
        )          #initialize the form using the data received.
        
        context = {
            'form': form,
            'form_action': form_action,
        }

        
        if form.is_valid(): # Validate form before saving.
            contact = form.save(commit=False) #create a contact without saving it immediately.
            contact.owner = request.user #Assign an authenticated user as the owner.
            contact.save() #Save the contact in the database.

            #Redirect the contact to the update contact page after successfull creation.
            return redirect(
                'contact:update', 
                contact_id=contact.pk
            ) 

        #Render the form with validation errors.
        return render(
            request,
            'contact/create.html',
            context
        )

    #instance an empty form for new contact creation.
    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }

    #render the contact creation page.
    return render(
        request,
        'contact/create.html',
        context
    ) 



#View for edit/update a already created contact
@login_required(login_url='contact:login') #Restricts access to authenticated users. Redirects to the login page if not logged in.
def update(request, contact_id):
    """
    Handle data manipulation of an already existing contact.

    This view allows the authenticated owner of a contact to edit its information.
    If the form submission is valid, the contact data is updated and the user is 
    redirected to the contact update page. Otherwise, the form is re-rendered with 
    validation errors.

    request:
        request (HttpRequest): The request object containing user data.
        contact_id (int): The ID of the contact to be updated.
    
    Returns:
        HttpResponseRedirect: Redirects to the contact update page if editing is successful.
        HttpResponse: Renders the contact creation form with errors if submission fails.

    """

    #Retrieve the contact object, ensuring it belongs to the authenticated user
    contact = get_object_or_404(
        Contact, 
        pk=contact_id, 
        show=True, 
        owner=request.user
    )

    # Define the URL for form submission
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST': #Check if the request method is POST
        form = ContactForm(request.POST, request.FILES, instance=contact) #Initialize form with contact data

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid(): # Validate form before saving
            contact = form.save() # Save the updated contact data
            return redirect(
                'contact:update', 
                contact_id=contact.pk
            ) # Redirect to the contact update page

        return render(
            request,
            'contact/create.html',
            context
        )  # Re-render form with validation errors

    # Initialize form with existing contact data for editing
    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    ) # Render the contact update form



#View for Delete a already created contact
@login_required(login_url='contact:login') #Restricts access to authenticated users. Redirects to the login page if not logged in.
def delete(request, contact_id):
    """
    Handle the exclusion of a contact.

    This view allows an authenticated user to permanently delete a contact they own. 
    The deletion only occurs if the user explicitly confirms the action.

    Args:
        request (HttpRequest): The request object containing user authentication and deletion request.
        contact_id (int): The ID of the contact to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the contact index page if deletion is successful.
        HttpResponse: Renders the contact page if confirmation is not provided.
    """

    #Retrieve the contact object, ensuring it belongs to the authenticated user
    contact = get_object_or_404(
        Contact, 
        pk=contact_id, 
        show=True, 
        owner=request.user
    )

    # Get confirmation from POST data, defaulting to 'no'
    confirmation = request.POST.get('confirmation', 'no')


    if confirmation == 'yes':  # Delete contact if confirmation is 'yes'
        contact.delete()
        return redirect('contact:index') # Redirect to contact list after deletion

     # Render contact page with deletion confirmation prompt
    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )