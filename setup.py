#!/usr/bin/env python
"""
سكريبت إعداد تلقائي لنظام إدارة المستندات
يقوم بإنشاء المجموعات والصلاحيات والمستخدمين التجريبيين
"""
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from documents.models import Document

def create_groups():
    """
    إنشاء مجموعات المستخدمين
    """
    print("⏳ جاري إنشاء المجموعات...")
    
    # الحصول على ContentType
    content_type = ContentType.objects.get_for_model(Document)
    
    # إنشاء مجموعة Admin
    admin_group, created = Group.objects.get_or_create(name='Admin')
    if created:
        print("✅ تم إنشاء مجموعة Admin")
    else:
        print("ℹ️  مجموعة Admin موجودة مسبقاً")
    
    # إضافة جميع الصلاحيات لـ Admin
    admin_permissions = Permission.objects.filter(content_type=content_type)
    admin_group.permissions.set(admin_permissions)
    print(f"   → تم إضافة {admin_group.permissions.count()} صلاحية")
    
    # إنشاء مجموعة Employee
    employee_group, created = Group.objects.get_or_create(name='Employee')
    if created:
        print("✅ تم إنشاء مجموعة Employee")
    else:
        print("ℹ️  مجموعة Employee موجودة مسبقاً")
    
    # إضافة صلاحيات للموظف (عرض، رفع، طباعة، تحميل)
    employee_permissions = Permission.objects.filter(
        content_type=content_type,
        codename__in=['view_document', 'add_document', 'print_document']
    )
    employee_group.permissions.set(employee_permissions)
    print(f"   → تم إضافة {employee_group.permissions.count()} صلاحية (عرض، رفع، طباعة)")
    
    return admin_group, employee_group

def create_demo_users(admin_group, employee_group):
    """
    إنشاء مستخدمين تجريبيين
    """
    print("\n⏳ جاري إنشاء المستخدمين التجريبيين...")
    
    users_data = [
        {
            'username': 'admin_demo',
            'email': 'admin@company.com',
            'first_name': 'مدير',
            'last_name': 'النظام',
            'password': 'admin123',
            'is_staff': True,
            'group': admin_group
        },
        {
            'username': 'employee1',
            'email': 'ahmed@company.com',
            'first_name': 'أحمد',
            'last_name': 'محمد',
            'password': 'emp123',
            'is_staff': False,
            'group': employee_group
        },
        {
            'username': 'employee2',
            'email': 'fatima@company.com',
            'first_name': 'فاطمة',
            'last_name': 'علي',
            'password': 'emp123',
            'is_staff': False,
            'group': employee_group
        },
    ]
    
    created_users = []
    
    for data in users_data:
        username = data.pop('username')
        password = data.pop('password')
        group = data.pop('group')
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults=data
        )
        
        if created:
            user.set_password(password)
            user.save()
            user.groups.add(group)
            print(f"✅ تم إنشاء المستخدم: {username} (كلمة المرور: {password})")
            created_users.append((username, password, group.name))
        else:
            print(f"ℹ️  المستخدم {username} موجود مسبقاً")
    
    return created_users

def print_summary(created_users):
    """
    عرض ملخص الإعداد
    """
    print("\n" + "="*60)
    print("✨ اكتمل الإعداد بنجاح!")
    print("="*60)
    
    if created_users:
        print("\n👥 المستخدمين التجريبيين:")
        print("-" * 60)
        for username, password, group in created_users:
            print(f"   اسم المستخدم: {username}")
            print(f"   كلمة المرور: {password}")
            print(f"   المجموعة: {group}")
            print("-" * 60)
    
    print("\n🚀 خطوات البدء:")
    print("   1. شغل السيرفر: python manage.py runserver")
    print("   2. افتح المتصفح: http://localhost:8000")
    print("   3. سجل دخول بأحد المستخدمين أعلاه")
    
    print("\n⚠️  تنبيه أمني:")
    print("   - هذه حسابات تجريبية فقط")
    print("   - غير كلمات المرور للإنتاج")
    print("   - احذف المستخدمين التجريبيين بعد الاختبار")
    
    print("\n📚 للمزيد من المعلومات:")
    print("   اقرأ دليل التثبيت والإعداد الكامل")
    print("="*60 + "\n")

def main():
    """
    الدالة الرئيسية
    """
    print("\n" + "="*60)
    print("🔧 سكريبت الإعداد التلقائي - نظام إدارة المستندات")
    print("="*60 + "\n")
    
    try:
        # إنشاء المجموعات
        admin_group, employee_group = create_groups()
        
        # إنشاء المستخدمين التجريبيين
        created_users = create_demo_users(admin_group, employee_group)
        
        # عرض الملخص
        print_summary(created_users)
        
    except Exception as e:
        print(f"\n❌ حدث خطأ: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()