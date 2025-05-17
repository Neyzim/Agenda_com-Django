from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """
    Represents a category for contacts.

    Attributes:
        name (str): The name of the category.
    """
    class Meta:
        verbose_name  = 'Category'
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    """
    Represents a contact entry.

    Attributes:
        first_name (str): Contact's first name.
        last_name (str): Contact's last name.
        phone (str): Contact's phone number.
        email (str): Contact's email address.
        created_date (datetime): Timestamp of when the contact was created.
        description (str): Additional information about the contact.
        show (bool): Whether the contact is visible or not.
        picture (ImageField): Contact's profile picture.
        category (Category): Category associated with the contact.
        owner (User): The user who owns the contact.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m')
    category = models.ForeignKey(
                                Category, 
                                 on_delete=models.SET_NULL, 
                                 blank=True, 
                                 null= True
                                )
    
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True)

    

 