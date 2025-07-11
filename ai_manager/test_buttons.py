from django.http import HttpResponse

def test_buttons_view(request):
    html_content = '''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تست دکمه‌های رنگی</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
    .action-btn {
        min-width: 90px;
        font-size: 0.875rem;
        font-weight: 500;
        border-radius: 0.375rem;
        transition: all 0.2s ease;
        padding: 0.375rem 0.75rem;
        border: none;
        cursor: pointer;
        margin: 4px;
    }
    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .btn-balance {
        background: linear-gradient(45deg, #17a2b8, #138496);
        color: white;
    }
    .btn-balance:hover {
        background: linear-gradient(45deg, #138496, #117a8b);
        color: white;
    }
    .btn-personal {
        background: linear-gradient(45deg, #6f42c1, #5a32a3);
        color: white;
    }
    .btn-personal:hover {
        background: linear-gradient(45deg, #5a32a3, #4c2a85);
        color: white;
    }
    .btn-prompt {
        background: linear-gradient(45deg, #28a745, #218838);
        color: white;
    }
    .btn-prompt:hover {
        background: linear-gradient(45deg, #218838, #1e7e34);
        color: white;
    }
    .btn-test {
        background: linear-gradient(45deg, #007bff, #0056b3);
        color: white;
    }
    .btn-test:hover {
        background: linear-gradient(45deg, #0056b3, #004085);
        color: white;
    }
    .btn-toggle {
        background: linear-gradient(45deg, #ffc107, #e0a800);
        color: #212529;
    }
    .btn-toggle:hover {
        background: linear-gradient(45deg, #e0a800, #d39e00);
        color: #212529;
    }
    .btn-delete {
        background: linear-gradient(45deg, #dc3545, #c82333);
        color: white;
    }
    .btn-delete:hover {
        background: linear-gradient(45deg, #c82333, #bd2130);
        color: white;
    }
    .table-actions {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
        align-items: center;
        justify-content: flex-start;
    }
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <h1 class="text-center mb-4">
                    <i class="bi bi-palette text-primary"></i>
                    تست دکمه‌های رنگی - بدون Login
                </h1>
                
                <div class="alert alert-success text-center">
                    <h4>✅ اگر دکمه‌های زیر رنگی هستند، CSS کار می‌کند!</h4>
                </div>
                
                <div class="card shadow">
                    <div class="card-header bg-primary text-white text-center">
                        <h5 class="mb-0">
                            <i class="bi bi-list-ul"></i>
                            نمونه API Keys با دکمه‌های رنگی
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover align-middle">
                                <thead class="table-light">
                                    <tr>
                                        <th><i class="bi bi-robot"></i> سرویس</th>
                                        <th><i class="bi bi-cpu"></i> مدل</th>
                                        <th><i class="bi bi-check-circle"></i> وضعیت</th>
                                        <th><i class="bi bi-gear"></i> عملیات</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>
                                            <i class="bi bi-chat-square-text text-primary me-2"></i>
                                            <strong>Claude (Anthropic)</strong>
                                        </td>
                                        <td>
                                            <code class="bg-light px-2 py-1 rounded">claude-sonnet-4-20250514</code>
                                        </td>
                                        <td>
                                            <span class="badge bg-success">
                                                <i class="bi bi-check-circle-fill"></i> فعال
                                            </span>
                                        </td>
                                        <td>
                                            <div class="table-actions">
                                                <button class="btn btn-balance action-btn btn-sm">
                                                    <i class="bi bi-wallet2"></i>
                                                    موجودی
                                                </button>
                                                
                                                <button class="btn btn-personal action-btn btn-sm">
                                                    <i class="bi bi-person-gear"></i>
                                                    شخصی
                                                </button>
                                                
                                                <button class="btn btn-prompt action-btn btn-sm">
                                                    <i class="bi bi-plus-circle"></i>
                                                    پرامپت
                                                </button>
                                                
                                                <button class="btn btn-test action-btn btn-sm">
                                                    <i class="bi bi-arrow-clockwise"></i>
                                                    تست
                                                </button>
                                                
                                                <button class="btn btn-toggle action-btn btn-sm">
                                                    <i class="bi bi-toggle-on"></i>
                                                    فعال
                                                </button>
                                                
                                                <button class="btn btn-delete action-btn btn-sm">
                                                    <i class="bi bi-trash"></i>
                                                    حذف
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <i class="bi bi-lightning text-success me-2"></i>
                                            <strong>OpenAI</strong>
                                        </td>
                                        <td>
                                            <code class="bg-light px-2 py-1 rounded">gpt-4o</code>
                                        </td>
                                        <td>
                                            <span class="badge bg-warning">
                                                <i class="bi bi-exclamation-triangle-fill"></i> تست نشده
                                            </span>
                                        </td>
                                        <td>
                                            <div class="table-actions">
                                                <button class="btn btn-balance action-btn btn-sm">
                                                    <i class="bi bi-wallet2"></i>
                                                    موجودی
                                                </button>
                                                
                                                <button class="btn btn-personal action-btn btn-sm">
                                                    <i class="bi bi-person-gear"></i>
                                                    شخصی
                                                </button>
                                                
                                                <button class="btn btn-prompt action-btn btn-sm">
                                                    <i class="bi bi-plus-circle"></i>
                                                    پرامپت
                                                </button>
                                                
                                                <button class="btn btn-test action-btn btn-sm">
                                                    <i class="bi bi-arrow-clockwise"></i>
                                                    تست
                                                </button>
                                                
                                                <button class="btn btn-toggle action-btn btn-sm">
                                                    <i class="bi bi-toggle-off"></i>
                                                    غیرفعال
                                                </button>
                                                
                                                <button class="btn btn-delete action-btn btn-sm">
                                                    <i class="bi bi-trash"></i>
                                                    حذف
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header bg-info text-white">
                        <h6 class="mb-0">
                            <i class="bi bi-info-circle"></i>
                            راهنمای رنگ‌ها
                        </h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>دکمه‌های عملیات:</h6>
                                <ul class="list-unstyled">
                                    <li><span class="badge" style="background: #17a2b8;">🔵</span> موجودی - آبی فیروزه‌ای</li>
                                    <li><span class="badge" style="background: #6f42c1;">🟣</span> شخصی - بنفش</li>
                                    <li><span class="badge" style="background: #28a745;">🟢</span> پرامپت - سبز</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6>دکمه‌های مدیریت:</h6>
                                <ul class="list-unstyled">
                                    <li><span class="badge" style="background: #007bff;">🔵</span> تست - آبی تیره</li>
                                    <li><span class="badge" style="background: #ffc107; color: #212529;">🟡</span> فعال/غیرفعال - زرد</li>
                                    <li><span class="badge" style="background: #dc3545;">🔴</span> حذف - قرمز</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="text-center mt-4">
                    <a href="/login/" class="btn btn-primary btn-lg">
                        <i class="bi bi-box-arrow-in-right"></i>
                        ورود برای دیدن صفحه اصلی
                    </a>
                    <a href="/ai-chat/" class="btn btn-secondary btn-lg">
                        <i class="bi bi-chat-text"></i>
                        چت AI
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // اضافه کردن effect کلیک برای دکمه‌ها
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 100);
            });
        });
    </script>
</body>
</html>'''
    return HttpResponse(html_content)
