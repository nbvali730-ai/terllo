from django.contrib import admin
from .models import Task, Notification

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'created_at')
    list_filter = ('status', 'assigned_to')

admin.site.register(Notification)
