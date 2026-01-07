// نظام إدارة المستندات - JavaScript الرئيسي

document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // Confirm delete
    const deleteButtons = document.querySelectorAll('.btn-danger[href*="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('هل أنت متأكد من الحذف؟')) {
                e.preventDefault();
            }
        });
    });
    
    // File input preview
    const fileInput = document.getElementById('id_file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            const fileSize = (e.target.files[0]?.size / 1024 / 1024).toFixed(2);
            
            if (fileName) {
                console.log(`تم اختيار: ${fileName} (${fileSize} MB)`);
                
                // Check file size
                if (fileSize > 10) {
                    alert('حجم الملف أكبر من 10 ميجابايت!');
                    e.target.value = '';
                }
            }
        });
    }
    
    // Search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.target.closest('form').submit();
            }
        });
    }
    
});

// Loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.id = 'loading-spinner';
    document.body.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) spinner.remove();
}