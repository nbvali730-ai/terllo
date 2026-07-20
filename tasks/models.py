from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# مدل تسک‌ها
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'برای انجام'),
        ('doing', 'در حال انجام'),
        ('done', 'انجام شده'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان کار")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks',
                                verbose_name="مدیر (سازنده)")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks',
                                    verbose_name="مسئول انجام (حسابدار)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo', verbose_name="وضعیت")

    # اضافه شد: برای حفظ ترتیب تسک‌ها در ستون‌ها
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # تنظیم کردیم که همیشه به صورت پیش‌فرض بر اساس ترتیب نمایش داده شوند
        ordering = ['order']

    def __str__(self):
        return self.title


# مدل نوتیفیکیشن
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


# مدل پروفایل کاربر برای تعیین نقش (ادمین، حسابدار، کارمند)
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'مدیر کل'),
        ('accountant', 'حسابدار'),
        ('staff', 'کارمند ساده'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


# سیگنال‌ها برای ساخت خودکار پروفایل بلافاصله بعد از ساخت کاربر
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
