from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Task, UserProfile
from .forms import AccountantRegistrationForm, TaskCreateForm

@login_required
def board_view(request):
    # اطمینان از وجود پروفایل
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_role = profile.role

    # تعیین کوئری پایه بر اساس نقش
    if user_role == 'admin':
        base_query = Task.objects.all()
    else:
        base_query = Task.objects.filter(assigned_to=request.user)

    # گرفتن تسک‌ها با احتیاط بیشتر در ترتیب
    # اگر فیلد order نداری، این رو به ('-created_at') تغییر بده
    tasks_todo = base_query.filter(status='todo')
    tasks_doing = base_query.filter(status='doing')
    tasks_done = base_query.filter(status='done')

    context = {
        'tasks_todo': tasks_todo,
        'tasks_doing': tasks_doing,
        'tasks_done': tasks_done,
        'user_profile': profile, # اضافه کردن پروفایل به کانتکست برای استفاده در تمپلیت
    }

    return render(request, 'tasks/board.html', context)

@csrf_exempt
@login_required
def update_task_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('new_status')

        try:
            task = Task.objects.get(id=task_id)
            profile, created = UserProfile.objects.get_or_create(user=request.user)

            if profile.role != 'admin' and task.assigned_to != request.user:
                return JsonResponse({'status': 'error', 'message': 'عدم دسترسی'})

            task.status = new_status
            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'تسک پیدا نشد'})

    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر'})

@login_required
def register_accountant(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.role != 'admin':
        raise PermissionDenied

    if request.method == 'POST':
        form = AccountantRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board')
    else:
        form = AccountantRegistrationForm()
    return render(request, 'tasks/register.html', {'form': form})

@login_required
def create_task(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.role != 'admin':
        raise PermissionDenied

    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.manager = request.user
            task.save()
            # بعد از ذخیره مستقیم میریم به میز کار
            return redirect('board')
    else:
        form = TaskCreateForm()
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def dashboard_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.role != 'admin':
        raise PermissionDenied

    total_tasks = Task.objects.count()
    todo_count = Task.objects.filter(status='todo').count()
    doing_count = Task.objects.filter(status='doing').count()
    done_count = Task.objects.filter(status='done').count()

    tasks_by_user = (
        Task.objects
        .values('assigned_to__username')
        .annotate(total=Count('id'))
    )

    progress = 0
    if total_tasks > 0:
        progress = int((done_count / total_tasks) * 100)

    context = {
        "total_tasks": total_tasks,
        "todo_count": todo_count,
        "doing_count": doing_count,
        "done_count": done_count,
        "tasks_by_user": tasks_by_user,
        "progress": progress
    }
    return render(request, "tasks/dashboard.html", context)
