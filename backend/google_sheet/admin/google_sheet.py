from django.contrib import admin
from ..models import SheetRow


@admin.register(SheetRow)
class SheetRowAdmin(admin.ModelAdmin):
    pass
