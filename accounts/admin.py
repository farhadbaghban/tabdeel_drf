from django.contrib import admin
from .models import User, DeletedUsers

admin.site.register(User)


@admin.register(DeletedUsers)
class DeactivatedUsers(admin.ModelAdmin):
    def get_queryset(self, request):
        return DeletedUsers.objects.filter(is_active=False)

    actions = [
        "recover",
    ]

    @admin.action(description="Recover Deleted User")
    def recover(self, request, queryset):
        queryset.update(is_active=True, de_activate_date=None)
