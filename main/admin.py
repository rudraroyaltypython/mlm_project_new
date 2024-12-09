from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_growth', 'earnings', 'referrals', 'is_retired')
    search_fields = ('user__username',)
    actions = ['mark_as_reviewed']  # Add an action to mark users as reviewed

    @admin.action(description='Mark selected users as reviewed')
    def mark_as_reviewed(self, request, queryset):
        queryset.update(is_new=True)

admin.site.register(UserProfile, UserProfileAdmin)
