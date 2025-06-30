from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Feedback
import csv
from django.http import HttpResponse

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    actions = ['export_as_csv']  # Add CSV export action

    # Define the action method
    def export_as_csv(self, request, queryset):
        # Set up HTTP response for CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="feedbacks.csv"'

        writer = csv.writer(response)
        # Header row
        writer.writerow(['Title', 'Description', 'Status', 'Created At', 'User Email'])

        # Data rows
        for feedback in queryset:
            writer.writerow([
                feedback.title,
                feedback.description,
                feedback.status,
                feedback.created_at,
                feedback.user.email
            ])

        return response

    export_as_csv.short_description = "Export selected feedbacks to CSV"