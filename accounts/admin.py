from django.contrib import admin
from .models import (
    CustomUserRegistration, 
    Department, 
    Perspective, 
    DepartmentalObjective, 
    StrategicResult, 
    PerformanceMeasure, 
    Target,
    DepartmentalInitiativeOrActivities, 
    Deliverable,
    InitialTemplateDetail,
    AchievementChallenge,
    Formula,
    ActualExpenditure,
)
from .forms import RegistrationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomAdmin(UserAdmin):
    add_form = RegistrationForm
    form = CustomUserChangeForm
    model = CustomUserRegistration
    list_display = [
        'username', 
        'first_name',
        'last_name',
        'email',
        'department',
        'is_strategy',
        'is_admin',
        'is_director',
        'is_work_plan_manager',
        'is_manager',
        'status',
    ]

    fieldsets = UserAdmin.fieldsets + (('User Details', {"fields": ('department', 'is_strategy', 'is_admin', 'is_director', 'is_work_plan_manager', 'is_manager', 'status',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('User Details', {"fields": ('first_name', 'last_name', 'email','department', 'is_strategy', 'is_admin', 'is_director', 'is_work_plan_manager', 'is_manager', 'status',)}),)

admin.site.register(CustomUserRegistration, CustomAdmin)
admin.site.register(Perspective)
admin.site.register(Department)
admin.site.register(DepartmentalObjective)
admin.site.register(StrategicResult)
admin.site.register(PerformanceMeasure)
admin.site.register(Target)
admin.site.register(DepartmentalInitiativeOrActivities)
admin.site.register(Deliverable)
admin.site.register(InitialTemplateDetail)
admin.site.register(AchievementChallenge)
admin.site.register(Formula)
admin.site.register(ActualExpenditure)

