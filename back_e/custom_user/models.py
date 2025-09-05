from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings
from django.utils.text import slugify
import os

# def upload_profile(instance,filename):
#     base, ext = os.path.splitext(filename)
#     clean_name = slugify(base)
#     return f"time_tally/profile/{instance.username}_{clean_name}{ext.lower()}"

class CustomUserManager(BaseUserManager):
    def create_user(self,email,username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("username is required")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active",True)

        user = self.model(username=username,email=email,**extra_fields)

        if password:
            user.set_password(password)

        else:
            user.set_unusable_password()
        
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email,username,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email,username,password, **extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=20,unique=True)
    email = models.EmailField(unique=True)
    social_id = models.CharField(max_length=255,blank=True,null=True)
    social_image = models.URLField(blank=True, null=True)
    is_social_account = models.BooleanField(default=False)
    auth_provider = models.CharField(
    max_length=20,
    choices=[("email", "Email"), ("google", "Google")],
    default="email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects =CustomUserManager()

    def __str__(self):
        return f"username : {self.username}, email : {self.email}"

    class Meta:
        ordering = ("created_at",)

class CustomerInfo(models.Model):
    email = models.EmailField(unique=True)  # Évite les doublons pour l'email marketing
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)  # Optionnel
    created_at = models.DateTimeField(auto_now_add=True)  # Pour savoir quand le client est arrivé
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.full_name}"

class UserVerification(models.Model):
    username=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(null=True,blank=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expiration = models.DateTimeField(blank=True, null=True)



class UserAction(models.Model):
    action = models.CharField(max_length=50,null=True,blank=True)
    object = models.CharField(max_length=50, null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action}"
    
class UserFeedback(models.Model):
    name = models.CharField(max_length=10,null=True,blank=True)
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)



class ContactForm(models.Model):
    email = models.EmailField()
    message = models.CharField(max_length=1000)

    def __str__(self):
        return f"email : {self.email} - message : {self.message}"
