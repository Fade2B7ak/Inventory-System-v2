from django.contrib import admin
from .models import NewUser, NewProduct

# Register your models here.
admin.site.register(NewUser)

admin.site.register(NewProduct)
