"""
Document views
"""
import os
import logging
import mimetypes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.db.models import Q
from .models import Document, DocumentAccessLog
from .forms import DocumentUploadForm

logger = logging.getLogger('documents')


def get_client_ip(request):
    """
    الحصول على IP المستخدم
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def log_document_access(document, user, action, request):
    """
    تسجيل الوصول للمستند
    """
    DocumentAccessLog.objects.create(
        document=document,
        user=user,
        action=action,
        ip_address=get_client_ip(request)
    )
    logger.info(f"{user.username} - {action} - {document.title}")


@login_required
def document_list(request):
    """
    عرض قائمة المستندات
    """
    search_query = request.GET.get('search', '')
    documents = Document.objects.all()

    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    context = {
        'documents': documents,
        'search_query': search_query,
        'can_upload': request.user.has_perm('documents.add_document'),
        'can_delete': request.user.has_perm('documents.delete_document'),
        'can_print': request.user.has_perm('documents.print_document'),
    }
    return render(request, 'documents/list.html', context)


@login_required
@permission_required('documents.add_document', raise_exception=True)
def document_upload(request):
    """
    رفع مستند جديد
    """
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()

            log_document_access(document, request.user, 'upload', request)
            messages.success(request, f'تم رفع المستند "{document.title}" بنجاح')
            return redirect('documents:list')
    else:
        form = DocumentUploadForm()

    return render(request, 'documents/upload.html', {'form': form})


@login_required
def document_view(request, pk):
    """
    عرض تفاصيل المستند
    """
    document = get_object_or_404(Document, pk=pk)
    document.increment_views()
    log_document_access(document, request.user, 'view', request)

    context = {
        'document': document,
        'can_delete': request.user.has_perm('documents.delete_document'),
        'can_print': request.user.has_perm('documents.print_document'),
    }
    return render(request, 'documents/view.html', context)


@login_required
def document_download(request, pk):
    """
    تحميل المستند (PDF أو صورة)
    """
    document = get_object_or_404(Document, pk=pk)

    if not document.file or not os.path.exists(document.file.path):
        raise Http404("الملف غير موجود")

    document.increment_downloads()
    log_document_access(document, request.user, 'download', request)

    content_type, _ = mimetypes.guess_type(document.file.path)
    if not content_type:
        content_type = 'application/octet-stream'

    response = FileResponse(
        open(document.file.path, 'rb'),
        content_type=content_type
    )
    response['Content-Disposition'] = (
        f'attachment; filename="{os.path.basename(document.file.name)}"'
    )
    return response


@login_required
@permission_required('documents.print_document', raise_exception=True)
def document_print(request, pk):
    """
    عرض / طباعة المستند (PDF أو صورة)
    """
    document = get_object_or_404(Document, pk=pk)

    if not document.file or not os.path.exists(document.file.path):
        raise Http404("الملف غير موجود")

    log_document_access(document, request.user, 'print', request)

    content_type, _ = mimetypes.guess_type(document.file.path)
    if not content_type:
        content_type = 'application/octet-stream'

    response = FileResponse(
        open(document.file.path, 'rb'),
        content_type=content_type
    )
    response['Content-Disposition'] = (
        f'inline; filename="{os.path.basename(document.file.name)}"'
    )
    return response


@login_required
@permission_required('documents.delete_document', raise_exception=True)
def document_delete(request, pk):
    """
    حذف المستند
    """
    document = get_object_or_404(Document, pk=pk)

    if request.method == 'POST':
        title = document.title
        log_document_access(document, request.user, 'delete', request)

        if document.file and os.path.exists(document.file.path):
            os.remove(document.file.path)

        document.delete()
        messages.success(request, f'تم حذف المستند "{title}" بنجاح')
        return redirect('documents:list')

    return render(request, 'documents/delete_confirm.html', {'document': document})

