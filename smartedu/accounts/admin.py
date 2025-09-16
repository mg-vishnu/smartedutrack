from django.contrib import admin

# Register your models here.
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ("username", "email", )
admin.site.register(User, CustomUserAdmin)
