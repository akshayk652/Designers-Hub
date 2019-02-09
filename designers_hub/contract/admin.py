from django.contrib import admin
from .models import Contract, ContractFile, Rating

admin.site.register(Contract)
admin.site.register(ContractFile)
admin.site.register(Rating)