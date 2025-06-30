from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager to handle user creation operations
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, username and password.
        
        Args:
            email: User's email address (required)
            username: User's display name
            password: User's password (optional)
            **extra_fields: Additional fields to be saved
        
        Returns:
            The created user instance
        """
        # Validate email is provided
        if not email:
            raise ValueError("Email is required")
        
        # Normalize email (converts domain part to lowercase)
        email = self.normalize_email(email)
        
        # Create new user instance but don't save it yet
        user = self.model(email=email, username=username, **extra_fields)
        
        # Handle password hashing
        user.set_password(password)
        
        # Save user to database (using=self._db ensures consistency in multi-db setup)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, username and password.
        
        Args:
            Same as create_user, but automatically sets admin privileges
        """
        # Ensure superuser has required permissions
        extra_fields.setdefault('is_staff', True)      # Can access admin site
        extra_fields.setdefault('is_superuser', True)  # Has all permissions
        
        # Create superuser using create_user method
        return self.create_user(email, username, password, **extra_fields)

# Custom User Model extending Django's base user classes
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the unique identifier instead of username
    
    Inherits from:
        - AbstractBaseUser: Provides core user fields and functionality
        - PermissionsMixin: Adds support for groups and permissions
    """
    # Core fields
    email = models.EmailField(unique=True)                 # Primary identifier
    username = models.CharField(max_length=150)            # Display name
    is_active = models.BooleanField(default=True)         # Can login
    is_staff = models.BooleanField(default=False)         # Can access admin site

    # Link to the custom manager
    objects = CustomUserManager()

    # Specify which field to use for login
    USERNAME_FIELD = 'email'             # Login using email
    
    # Additional fields required when creating a user via CLI
    REQUIRED_FIELDS = ['username']       # Required when creating superuser

    def __str__(self):
        """String representation of user"""
        return self.email