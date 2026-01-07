"""
Document models
"""
import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone

def document_upload_path(instance, filename):
    """
    تحديد مسار حفظ الملف
    """
    date = timezone.now()
    return f'documents/{date.year}/{date.month:02d}/{filename}'

class Document(models.Model):
    """
    نموذج المستند
    """
    title = models.CharField('العنوان', max_length=200)
    description = models.TextField('الوصف', blank=True)
    file = models.FileField(
        'الملف',
        upload_to=document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='ملفات PDF فقط (أقصى حجم 10MB)'
    )
    
    # Metadata
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='uploaded_documents',
        verbose_name='رفع بواسطة'
    )
    uploaded_at = models.DateTimeField('تاريخ الرفع', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    
    # File info
    file_size = models.IntegerField('حجم الملف (بايت)', default=0)
    pages_count = models.IntegerField('عدد الصفحات', default=0, blank=True)
    
    # Access tracking
    views_count = models.IntegerField('عدد المشاهدات', default=0)
    downloads_count = models.IntegerField('عدد التحميلات', default=0)
    
    class Meta:
        verbose_name = 'مستند'
        verbose_name_plural = 'المستندات'
        ordering = ['-uploaded_at']
        permissions = [
            ('print_document', 'يمكنه طباعة المستندات'),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        حفظ حجم الملف عند الرفع
        """
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
    
    def get_file_size_display(self):
        """
        عرض حجم الملف بشكل قابل للقراءة
        """
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def increment_views(self):
        """
        زيادة عداد المشاهدات
        """
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_downloads(self):
        """
        زيادة عداد التحميلات
        """
        self.downloads_count += 1
        self.save(update_fields=['downloads_count'])


class DocumentAccessLog(models.Model):
    """
    سجل الوصول للمستندات
    """
    ACTION_CHOICES = [
        ('view', 'مشاهدة'),
        ('download', 'تحميل'),
        ('print', 'طباعة'),
        ('delete', 'حذف'),
    ]
    
    document = models.ForeignKey(
        Document, 
        on_delete=models.CASCADE, 
        related_name='access_logs',
        verbose_name='المستند'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='المستخدم'
    )
    action = models.CharField('الإجراء', max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField('التاريخ والوقت', auto_now_add=True)
    ip_address = models.GenericIPAddressField('عنوان IP', null=True, blank=True)
    
    class Meta:
        verbose_name = 'سجل وصول'
        verbose_name_plural = 'سجلات الوصول'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.document.title}"