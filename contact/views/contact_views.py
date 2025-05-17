from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    """
    Displays a paginated list of contacts.

    Args:
        request (HttpRequest): The request object containing user data.

    Returns:
        HttpResponse: Renders the main contacts page with paginated contact list.
    """
 
    # Get all visible contacts sorted by ID in descending order
    contacts = Contact.objects \
        .filter(show=True)\
        .order_by('-id')
    
    # Paginate contacts (10 per page)
    paginator = Paginator(contacts, 10)

    # Get the current page number from request
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    # Prepare context for rendering   
    context = {
        "page_obj": page_obj,
        'site_title': "Contatos - "
    }

    # Render the main contacts page with pagination
    return render(
        request,
        'contact/main.html',
        context,
    )

def contact(request, contact_id):
    """
    Displays a single contact's details.

    Args:
        request (HttpRequest): The request object containing user data.
        contact_id (int): The ID of the contact to display.

    Returns:
        HttpResponse: Renders the contact detail page.
    """
    # Retrieve the contact object or return a 404 error if not found
    single_contact = get_object_or_404(
    Contact, pk=contact_id, show=True
    )

    # Construct site title with contact's name
    site_title = f"{single_contact.first_name} {single_contact.last_name} - "

    # Prepare context with contact data
    context = {
        'contact': single_contact,
        'site_title': site_title,
    }

    # Render contact details page
    return render(
        request,
        "contact/contact.html",
        context,
    )

def search(request):
    """
    Searches for contacts based on user input.

    Args:
        request (HttpRequest): The request object containing search query.

    Returns:
        HttpResponseRedirect: Redirects to the contact index if search query is empty.
        HttpResponse: Renders the search results page with matched contacts.
    """

    # Get search query from request and remove extra spaces
    search_value = request.GET.get("q", '').strip()

    # Redirect to index if search query is empty
    if search_value == "":
        return redirect("contact:index")

    # Filter contacts based on search query (partial match)
    contacts = Contact.objects \
        .filter(show=True)\
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value)

            ) \
        .order_by('-id')

    # Paginate results (10 per page)
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    # Prepare context with search results
    context = {
        "page_obj": page_obj,
        'site_title': "Contatos - ",
        'search_value': search_value
    }

    # Render search results page
    return render(
        request,
        'contact/main.html',
        context,
    )

