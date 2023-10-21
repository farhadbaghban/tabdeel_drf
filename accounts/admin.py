from django.contrib import admin
from .models import User, DeletedUsers

admin.site.register(User)


@admin.register(DeletedUsers)
class DeactivatedUsers(admin.ModelAdmin):
    actions = [
        "recover",
    ]

    @admin.action(description="Recover Deleted User")
    def recover(self, request, queryset):
        queryset.update(is_active=True, de_activate_date=None)
