"""
Accounts models
"""
from django.db import models
from django.contrib.auth.models import User

# نستخدم User الجاهز من Django
# يمكن إضافة Profile إذا احتجنا معلومات إضافية

class UserProfile(models.Model):
    """
    ملف تعريف المستخدم - معلومات إضافية
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('رقم الهاتف', max_length=20, blank=True)
    department = models.CharField('القسم', max_length=100, blank=True)
    employee_id = models.CharField('رقم الموظف', max_length=50, blank=True, unique=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    
    class Meta:
        verbose_name = 'ملف تعريف'
        verbose_name_plural = 'ملفات التعريف'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"