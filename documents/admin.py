"""
Admin configuration for Documents
"""
from django.contrib import admin
from .models import Document, DocumentAccessLog

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    إدارة المستندات
    """
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'file_size_display', 'views_count', 'downloads_count')
    list_filter = ('uploaded_at', 'uploaded_by')
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_at', 'updated_at', 'file_size', 'views_count', 'downloads_count')
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('معلومات المستند', {
            'fields': ('title', 'description', 'file')
        }),
        ('معلومات الرفع', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at')
        }),
        ('إحصائيات', {
            'fields': ('file_size', 'pages_count', 'views_count', 'downloads_count')
        }),
    )
    
    def file_size_display(self, obj):
        return obj.get_file_size_display()
    file_size_display.short_description = 'حجم الملف'
    
    def save_model(self, request, obj, form, change):
        """
        تعيين المستخدم الذي رفع الملف
        """
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DocumentAccessLog)
class DocumentAccessLogAdmin(admin.ModelAdmin):
    """
    إدارة سجلات الوصول
    """
    list_display = ('document', 'user', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('document__title', 'user__username')
    readonly_fields = ('document', 'user', 'action', 'timestamp', 'ip_address')
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser