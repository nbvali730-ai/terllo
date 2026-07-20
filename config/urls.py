from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
# تغییر اینجا: ایمپورت کردن کل ماژول views برای راحتی بیشتر
from tasks import views

urlpatterns = [
    # مسیر پنل مدیریت اصلی جنگو
    path('admin/', admin.site.urls),

    # صفحه اصلی میز کار (Board)
    path('', views.board_view, name='board'),

    # مسیر آپدیت وضعیت تسک‌ها (برای Drag & Drop)
    path('update-task-status/', views.update_task_status, name='update_task_status'),

    # مسیر ثبت‌نام کاربر جدید (فقط برای مدیر)
    path('register/', views.register_accountant, name='register'),

    # مسیر ایجاد تسک جدید (فقط برای مدیر)
    path('task/create/', views.create_task, name='create_task'),

    # مسیر داشبورد مدیریتی
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # مسیرهای ورود و خروج
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
