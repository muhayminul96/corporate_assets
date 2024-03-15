from django.contrib import admin

# Register your models here.

from .models import Company, Employee, Asset, AssetLog

admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Asset)
admin.site.register(AssetLog)
