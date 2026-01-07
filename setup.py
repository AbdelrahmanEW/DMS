#!/usr/bin/env python
"""
Automatic setup script for Document Management System
Creates groups, permissions, and demo users
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from documents.models import Document

def create_groups():
    """
    Create user groups
    """
    print("⏳ Creating groups...")
    
    # Get ContentType
    content_type = ContentType.objects.get_for_model(Document)
    
    # Create Admin group
    admin_group, created = Group.objects.get_or_create(name='Admin')
    if created:
        print("✅ Admin group created")
    else:
        print("ℹ️  Admin group already exists")
    
    # Add all permissions to Admin
    admin_permissions = Permission.objects.filter(content_type=content_type)
    admin_group.permissions.set(admin_permissions)
    print(f"   → Added {admin_group.permissions.count()} permissions")
    
    # Create Employee group
    employee_group, created = Group.objects.get_or_create(name='Employee')
    if created:
        print("✅ Employee group created")
    else:
        print("ℹ️  Employee group already exists")
    
    # Add permissions to Employee (view, add, print)
    employee_permissions = Permission.objects.filter(
        content_type=content_type,
        codename__in=['view_document', 'add_document', 'print_document']
    )
    employee_group.permissions.set(employee_permissions)
    print(f"   → Added {employee_group.permissions.count()} permissions (view, add, print)")
    
    return admin_group, employee_group

def create_demo_users(admin_group, employee_group):
    """
    Create demo users
    """
    print("\n⏳ Creating demo users...")
    
    users_data = [
        {
            'username': 'admin_demo',
            'email': 'admin@company.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'password': 'admin123',
            'is_staff': True,
            'group': admin_group
        },
        {
            'username': 'employee1',
            'email': 'ahmed@company.com',
            'first_name': 'Ahmed',
            'last_name': 'Mohamed',
            'password': 'emp123',
            'is_staff': False,
            'group': employee_group
        },
        {
            'username': 'employee2',
            'email': 'fatima@company.com',
            'first_name': 'Fatima',
            'last_name': 'Ali',
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
            print(f"✅ User created: {username} (password: {password})")
            created_users.append((username, password, group.name))
        else:
            print(f"ℹ️  User {username} already exists")
    
    return created_users

def print_summary(created_users):
    """
    Print setup summary
    """
    print("\n" + "="*60)
    print("✨ Setup completed successfully!")
    print("="*60)
    
    if created_users:
        print("\n👥 Demo Users:")
        print("-" * 60)
        for username, password, group in created_users:
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            print(f"   Group: {group}")
            print("-" * 60)
    
    print("\n🚀 Next Steps:")
    print("   1. Start server: python manage.py runserver")
    print("   2. Open browser: http://localhost:8000")
    print("   3. Login with one of the users above")
    
    print("\n⚠️  Security Warning:")
    print("   - These are demo accounts only")
    print("   - Change passwords for production")
    print("   - Delete demo users after testing")
    
    print("\n📚 For more information:")
    print("   Read the complete installation guide")
    print("="*60 + "\n")

def main():
    """
    Main function
    """
    print("\n" + "="*60)
    print("🔧 Automatic Setup - Document Management System")
    print("="*60 + "\n")
    
    try:
        # Create groups
        admin_group, employee_group = create_groups()
        
        # Create demo users
        created_users = create_demo_users(admin_group, employee_group)
        
        # Print summary
        print_summary(created_users)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()