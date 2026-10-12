from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Subject, Doubt


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'name', 'role', 'register_number', 'teacher_id', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'name', 'register_number', 'teacher_id')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Profile Fields', {
            'fields': ('role', 'name', 'register_number', 'teacher_id')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Profile Fields', {
            'fields': ('role', 'name', 'register_number', 'teacher_id')
        }),
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')


@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'status', 'created_at', 'answered_by', 'answered_at')
    list_filter = ('status', 'subject', 'created_at')
    search_fields = ('student__name', 'student__register_number', 'question', 'teacher_answer')
