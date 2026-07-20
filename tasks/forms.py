from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Task


class AccountantRegistrationForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        label="نقش کاربر",
        initial='accountant'
    )
    password = forms.CharField(widget=forms.PasswordInput(), label="رمز عبور")

    # اسم فیلد رو عوض کردم که هیچ ولیدیشن اتوماتیکی روش اجرا نشه
    mobile_number = forms.CharField(
        label="شماره موبایل",
        required=True,
        widget=forms.TextInput(attrs={'type': 'text'})
    )

    class Meta:
        model = User
        # فیلد email رو از اینجا حذف کردم
        fields = ['username', 'first_name', 'last_name', 'password']
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-rose-500 transition-all',
                'placeholder': f'{field.label} را وارد کنید...'
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # اینجا شماره موبایل رو دستی می‌ریزیم توی فیلد ایمیل دیتابیس
        user.email = self.cleaned_data.get('mobile_number')

        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data['role']
            profile.save()
        return user


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to']
        labels = {
            'title': 'عنوان وظیفه',
            'description': 'توضیحات',
            'status': 'وضعیت اولیه',
            'assigned_to': 'ارجاع به کاربر',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none transition-all bg-gray-50'
            })
