from django.contrib import admin
from contact import models

# Register your models here.

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Contact model.

    - Displays key contact details in the admin list view.
    - Enables ordering by ID.
    - Allows searching by ID, first name, and last name.
    """

    list_display = (
        'id',
        'first_name',
        'last_name',
        'phone',
        'email',
        )
    ordering = (
        'id',)
    search_fields = ('id', 'first_name', 'last_name',)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Category model.

    - Displays the category name in the admin list view.
    - Enables ordering by ID.
    """
     
    list_display = ('name',)
    ordering = ('id',)