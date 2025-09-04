from django.contrib import admin
from .models import CustomUser,UserAction,ContactForm,UserVerification

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display= ("username","email",)

@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ("verification_code","username","email",)




@admin.register(UserAction)
class userActionAdmin(admin.ModelAdmin):
    list_display = ("action","object","timestamp",)


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("email","message",)