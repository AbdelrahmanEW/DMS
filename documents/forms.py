"""
Document forms
"""
from django import forms
from .models import Document
import os

class DocumentUploadForm(forms.ModelForm):
    """
    نموذج رفع المستندات (PDF + Images)
    """
    class Meta:
        model = Document
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان المستند'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'وصف المستند (اختياري)'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png,.gif'
            }),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            ext = os.path.splitext(file.name)[1].lower()

            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif']

            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    'الملف يجب أن يكون PDF أو صورة (JPG, PNG, GIF)'
                )

            # الحجم الأقصى 10MB
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(
                    'حجم الملف يجب أن لا يتجاوز 10 ميجابايت'
                )

        return file



# """
# Document forms
# """
# from django import forms
# from .models import Document

# class DocumentUploadForm(forms.ModelForm):
#     """
#     نموذج رفع المستندات
#     """
#     class Meta:
#         model = Document
#         fields = ['title', 'description', 'file']
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'عنوان المستند'
#             }),
#             'description': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 4,
#                 'placeholder': 'وصف المستند (اختياري)'
#             }),
#             'file': forms.FileInput(attrs={
#                 'class': 'form-control',
#                 'accept': '.pdf'
#             }),
#         }
    
#     def clean_file(self):
#         """
#         التحقق من نوع وحجم الملف
#         """
#         file = self.cleaned_data.get('file')
        
#         if file:
#             # التحقق من الامتداد
#             if not file.name.endswith('.pdf'):
#                 raise forms.ValidationError('يجب أن يكون الملف من نوع PDF')
            
#             # التحقق من الحجم (10MB)
#             if file.size > 10 * 1024 * 1024:
#                 raise forms.ValidationError('حجم الملف يجب أن لا يتجاوز 10 ميجابايت')
        
#         return file