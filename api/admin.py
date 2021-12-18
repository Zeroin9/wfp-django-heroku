from django.contrib import admin
from .models import Parcel, Operation, Token, ParcelTokenLink

# Register your models here.
admin.site.register(Parcel)
admin.site.register(Operation)
admin.site.register(Token)
admin.site.register(ParcelTokenLink)