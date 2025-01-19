from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceRequest

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'request_type', 'status', 'created_at', 'updated_at', 'view_attachment')
    list_filter = ('status', 'request_type')
    search_fields = ('user__username', 'details')

    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(status='Completed')  
        self.message_user(request, "Selected requests marked as resolved.")

    mark_resolved.short_description = "Mark selected requests as resolved"

    
    def view_attachment(self, obj):
        if obj.attachment:
            return format_html('<a href="{0}" target="_blank">View Attachment</a>', obj.attachment.url)
        return "No Attachment"
    view_attachment.short_description = 'Attachment'

admin.site.register(ServiceRequest, ServiceRequestAdmin)
