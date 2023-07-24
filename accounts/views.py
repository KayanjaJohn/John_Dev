from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from .helpers import send_forget_password_mail
from .forms import *
from .forms import (
    RegistrationForm, 
    DepartmentalObjectiveForm, 
    StrategicResultForm, 
    PerformanceMeasureForm, 
    TargetsForm, 
    DepartmentalInitiativeOrActivitiesForm, 
    DeliverableForm,
    FormulaForm,
    PerformanceMeasureActualResultsForm,
    ActualExpenditureForm,
    InitialTemplateDetailForm,
    ManagerDirectorTemplateForm,
    AchievementChallengeForm,
)
from .models import (
    Perspective, 
    DepartmentalObjective, 
    CustomUserRegistration, 
    Department, 
    StrategicResult, 
    PerformanceMeasure, 
    Target, 
    DepartmentalInitiativeOrActivities, 
    Deliverable,
    Formula,
    PerformanceMeasureActualResults,
    ActualExpenditure,
    InitialTemplateDetail,
    AchievementChallenge,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, admin_user
from django.contrib import messages
from .models import *
from django.urls import reverse
from .forms import *
import xlwt
from django.http import HttpResponse


# Login
def userLogin(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None and not user.is_superuser:
                if user.status == 'Blocked':
                    messages.error(request, 'Sorry, you are currently blocked. Please contact our technical person for assistance.')
                    return redirect('userLogin')  # Redirect back to the login page with the message

                login(request, user)
                if user.is_admin or user.is_superuser:
                    return redirect('adminDashboard' + '/?menu=Dashboard')
                elif user.is_director:
                    return redirect('directorDashboard' + '/?menu=Dashboard')
                elif user.is_work_plan_manager:
                    return redirect('workPlanManagerDashboard' + '/?menu=Dashboard&perspective=Customer')
                elif user.is_strategy:
                    return redirect('strategyDashboard' + '/?menu=Dashboard')
                elif user.is_manager:
                    return redirect('managerDashboard' + '/?menu=Dashboard')
            else:
                messages.error(request, 'Unknown user, please fill in the correct information to view the dashboard.')
                return redirect('userLogin')  # Redirect back to the login page with the message

    except Exception as e:
        print(e)
        messages.error(request, 'Failed to log in.')
    return render(request, 'userLogin.html')


    
#Logout
def userLogout(request):
    logout(request)
    return redirect('userLogin')

# User information
from django.db.models import Q
@login_required(login_url='userLogin')
def users_info(request):
    current_date = timezone.now().date()
    members = CustomUserRegistration.objects.filter(
        Q(is_strategy=True) | Q(is_manager=True) | Q(is_work_plan_manager=True) | Q(is_director=True)
    )
    for member in members:
        if member.disconnect_date and member.disconnect_date <= current_date:
            member.status = 'Blocked'
            member.save()
        else:
            member.status = 'Active'
    context = {
        'members': members,
    }
    return render(request, 'users-info.html', context)




# REGISTRATION
@login_required(login_url='userLogin')
@admin_user
def userRegistration(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Registered successfully!')
            return redirect('userRegistration')

    context = {'form': form}

    return render(request, 'userRegistration.html', context)



# UPDATE_REGISTRATION
@login_required(login_url='userLogin')
def update_member(request, pk):
    member = get_object_or_404(CustomUserRegistration, pk=pk)

    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = UpdateForm(instance=member)

    context = {
        'form': form,
    }
    return render(request, 'Update_info.html', context)

# DELETE
def delete_member(request, pk):
    if request.method == 'POST':
        member = get_object_or_404(CustomUserRegistration, pk=pk)
        member.delete()
    return redirect('users')

# Admin Dashboard
from .models import Department
from django.db.models import Count
from .forms import RegistrationForm
from django.db.models import Q
@login_required(login_url='userLogin')
def adminDashboard(request):
    current_date = timezone.now().date()

    # Filter the registered users based on their roles
    registered_users = CustomUserRegistration.objects.filter(
        Q(is_strategy=True) | Q(is_manager=True) | Q(is_work_plan_manager=True) | Q(is_director=True)
    )
    # Count the total number of registered users whose roles are among the ones outlined
    user_count = registered_users.count()
    department_count = Department.objects.count()
    active_user_count = registered_users.filter(status='Active').count()
    blocked_user_count = registered_users.filter(status='Blocked').count()
    role_counts = {
        'Strategy': registered_users.filter(is_strategy=True).count(),
        'Admin': registered_users.filter(is_admin=True).count(),
        'Director': registered_users.filter(is_director=True).count(),
        'work_plan_manager': registered_users.filter(is_work_plan_manager=True).count(),
        'Manager': registered_users.filter(is_manager=True).count(),
    }

    context = {
        'user_count': user_count,
        'department_count': department_count,
        'role_counts': role_counts,
        'active_user_count': active_user_count,
        'blocked_user_count': blocked_user_count,
    }

    return render(request, 'adminDashboard.html', context)




@login_required(login_url='userLogin')
def directorDashboard(request):
    return render(request, 'directorDashboard.html')

    # STATISTICAL DATA ANALYSIS
    

def statistical_data(objectives, strategic_results, performance_measures, departmental_activities, deliverables):
    #Initial variables
    number_of_objectives = []
    number_of_activities = []
    number_of_deliverables = []
    number_of_assigned_deliverables = []
    number_of_pending_deliverables = []
    number_of_completed_deliverables = []
    number_of_in_progress_deliverables = []
    number_of_pending_activities = []
    number_of_in_progress_activities = []
    number_of_completed_activities = []
    activities_in_progress = []
    
    activities_count = departmental_activities.count()
    complete_activities_list = []
    completed_activities = 0
    
    
    for objective in objectives:
        number_of_objectives.append(objective)
        for strategic_result in strategic_results:
            if strategic_result.departmental_objective == objective:
                for performance_measure in performance_measures:
                    if performance_measure.strategic_result == strategic_result:
                        for departmental_initiative in departmental_activities:
                            if departmental_initiative.performance_measure == performance_measure:
                                number_of_activities.append(departmental_initiative)
                                if departmental_initiative.activity_status == 'Pending':
                                    number_of_pending_activities.append(departmental_initiative)
                                elif departmental_initiative.activity_status == 'In progress':#Depends on all deliverables in this activity with a status of in progress
                                    number_of_in_progress_activities.append(departmental_initiative)
                                elif departmental_initiative.activity_status == 'Done':#Depends on all completed deliverables
                                    number_of_completed_activities.append(departmental_initiative)
                                for deliverable in deliverables:
                                    if deliverable.departmentalInitiativeOrActivity == departmental_initiative:
                                        number_of_deliverables.append(deliverable)
                                        if deliverable.lead_person != 'Not Assigned':
                                            number_of_assigned_deliverables.append(deliverable)
                                        if deliverable.deliverable_status == 'Pending':
                                            number_of_pending_deliverables.append(deliverable)
                                        elif deliverable.deliverable_status == 'In progress':
                                            number_of_in_progress_deliverables.append(deliverable)
                                            if deliverable.departmentalInitiativeOrActivity not in activities_in_progress:
                                                activities_in_progress.append(deliverable.departmentalInitiativeOrActivity) 
                                        elif deliverable.deliverable_status == 'Done':
                                            number_of_completed_deliverables.append(deliverable)
                                            if deliverable.departmentalInitiativeOrActivity not in complete_activities_list:
                                                complete_activities_list.append(deliverable.departmentalInitiativeOrActivity)
                                            
    if activities_count == len(complete_activities_list):
        completed_activities = activities_count
                                            
    return {
        'number_of_objectives': len(number_of_objectives),
        'number_of_activities': len(number_of_activities),
        'number_of_deliverables': len(number_of_deliverables),
        'number_of_pending_deliverables': len(number_of_pending_deliverables),
        'number_of_in_progress_deliverables': len(number_of_in_progress_deliverables),
        'number_of_completed_deliverables': len(number_of_completed_deliverables),
        'number_of_assigned_deliverables': len(number_of_assigned_deliverables),
        'number_of_pending_activities': len(number_of_pending_activities),
        'number_of_in_progress_activities': len(activities_in_progress),
        'number_of_completed_activities': completed_activities,
    }

@login_required(login_url='userLogin')
def workPlanManagerDashboard(request):
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    menu = request.GET.get('menu')
    perspective = Perspective.objects.none()
    managerDirectorTemplateForm = ManagerDirectorTemplateForm()
    department = Department.objects.get(department=request.user.department)
    created_by = CustomUserRegistration.objects.get(id=request.user.id)
    
    # GET MODEL DATA
    get_perspectives = Perspective.objects.all()#these are the listed perspectives
    department_statistics_per_perspective = {}
    
    departmental_objectives_per_perspective = DepartmentalObjective.objects.none()
    departmentalObjectives = DepartmentalObjective.objects.none()
    strategic_results = StrategicResult.objects.all()
    performance_measures = PerformanceMeasure.objects.all()
    departmental_initiatives = DepartmentalInitiativeOrActivities.objects.all()
    deliverables = Deliverable.objects.all()
    
    if initialTemplate:
        department_template_exists_in_initial_template = InitialTemplateDetail.objects.filter(department=department, template_Name=initialTemplate.template_Name).first()
        if not department_template_exists_in_initial_template:
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    
    if request.GET.get('perspective'):
        perspective = Perspective.objects.get(perspective=request.GET.get('perspective'))
        if not department_template_exists_in_initial_template:
            departmental_objectives_per_perspective = DepartmentalObjective.objects.none()
        else:
            departmental_objectives_per_perspective = DepartmentalObjective.objects.filter(department=department, perspective=perspective.id, template_name=department_template_exists_in_initial_template.id)
    else:
        if not department_template_exists_in_initial_template:
            departmentalObjectives = DepartmentalObjective.objects.none()
        else:
            departmentalObjectives = DepartmentalObjective.objects.filter(department=department, template_name=department_template_exists_in_initial_template.id)
    
    department_statistics = statistical_data(departmentalObjectives, strategic_results, performance_measures, departmental_initiatives, deliverables)
    department_statistics_per_perspective = statistical_data(departmental_objectives_per_perspective, strategic_results, performance_measures, departmental_initiatives, deliverables)

    if request.method == 'POST':
        if request.POST.get('changeTempStatusBtn') == 'changeTempStatus':
            managerDirectorTemplateForm = ManagerDirectorTemplateForm(request.POST)
            template_Status = request.POST.get('template_Status')
            print(template_Status)
            if managerDirectorTemplateForm.is_valid():
                managerDirectorTemplateFormInstance = managerDirectorTemplateForm.save(commit=False)
                managerDirectorTemplateFormInstance.template_Name = initialTemplate.template_Name
                managerDirectorTemplateFormInstance.template_Status = template_Status
                managerDirectorTemplateFormInstance.financial_Year_Starts = initialTemplate.financial_Year_Starts
                managerDirectorTemplateFormInstance.financial_Year_Ends = initialTemplate.financial_Year_Ends
                managerDirectorTemplateFormInstance.department = department
                managerDirectorTemplateFormInstance.created_by = created_by

                managerDirectorTemplateFormInstance.save()

                return redirect(reverse('workPlanManagerDashboard') + '?menu=' + menu)

            else:
                print('Form invalid')
        elif request.POST.get('updateTempStatusBtn') == 'updateTempStatus':
            current_department_template = InitialTemplateDetail.objects.get(id=request.POST.get('department_template_exists_in_initial_template_update'))
            template_Status = request.POST.get('template_Status')
            directorTemplateForm = ManagerDirectorTemplateForm(request.POST, instance=current_department_template)
            
            if directorTemplateForm.is_valid():
                directorTemplateFormInstance = directorTemplateForm.save(commit=False)
                directorTemplateFormInstance.template_Status = template_Status
                directorTemplateFormInstance.save()
                
                print('passed')
                return redirect(reverse('workPlanManagerDashboard') + '?menu=' + menu)
            else:
                print('Update Failed')

    context = {
        'menu': menu,
        'perspectives': get_perspectives,
        'initialTemplate': initialTemplate,
        'managerDirectorTemplateForm': managerDirectorTemplateForm,
        'department_template_exists_in_initial_template': department_template_exists_in_initial_template,
        'department_statistics': department_statistics,
        'department_statistics_per_perspective': department_statistics_per_perspective
        
    }
    return render(request, 'workPlanManagerDashboard.html', context)

@login_required(login_url='userLogin')
def strategyDashboard(request):
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    accepted_department_templates = InitialTemplateDetail.objects.none()
    department_templates_in_progress = InitialTemplateDetail.objects.none()
    department_templates_submitted = InitialTemplateDetail.objects.none()
    menu = request.GET.get('menu')
    perspective = Perspective.objects.none()
    department = Department.objects.get(department=request.user.department)
    get_perspectives = Perspective.objects.all()#these are the listed perspectives
    departments = Department.objects.all().count()
    
    
    if not initialTemplate:
        initialTemplate = InitialTemplateDetail.objects.none()
    else:
        accepted_department_templates = InitialTemplateDetail.objects.filter(template_Status='in progress') | InitialTemplateDetail.objects.filter(template_Status='closed')
        department_templates_in_progress = InitialTemplateDetail.objects.filter(template_Status='in progress')
        department_templates_submitted = InitialTemplateDetail.objects.filter(template_Status='closed')
    
    print(accepted_department_templates.count())
    print(departments)
    
    templateForm = InitialTemplateDetailForm()
    logged_in_user = CustomUserRegistration.objects.get(id=request.user.id)
    

    if request.method == 'POST':
        if request.POST.get('createTmpt') == 'createTmpt':
            # check for open templates
            open_templates = InitialTemplateDetail.objects.all()
            
            for temp_open in open_templates:
                if temp_open.template_Status == 'open':
                    temp_open.template_Status = 'close'
                    temp_open.save()
                elif temp_open.template_Status == 'in progress':
                    temp_open.template_Status = 'queued'
                    temp_open.save()
            
            templateForm = InitialTemplateDetailForm(request.POST)
            template_status = request.POST.get('template_status')

            if templateForm.is_valid():
                templateFormInstance = templateForm.save(commit=False)
                templateFormInstance.template_Status = template_status
                templateFormInstance.created_by = logged_in_user
                templateFormInstance.user_is_strategy = logged_in_user.is_strategy
                templateFormInstance.save()
                return redirect(reverse('strategyDashboard') + '?menu=' + menu)
        elif request.POST.get('closeTmpt') == 'closeTmpt':
            open_template = InitialTemplateDetail.objects.get(id=request.POST.get('template_id'))
            open_template.template_Status = 'closed'
            open_template.save()
            return redirect(reverse('strategyDashboard') + '?menu=' + menu)
        elif request.POST.get('rejectTmpt') == 'rejectTmpt':
            return redirect(reverse('strategyDashboard') + '?menu=' + menu)
    
    context = {
        'menu': menu,
        'perspectives': get_perspectives,
        'initialTemplate': initialTemplate,
        'templateForm': templateForm,
        'templates_in_progress': department_templates_in_progress.count(),
        'templates_submitted': department_templates_submitted.count(),
        'number_of_departments': departments,
        'accepted_templates': accepted_department_templates.count(),
    }
    return render(request, 'strategyDashboard.html', context)

@login_required(login_url='userLogin')
def managerDashboard(request):
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    menu = request.GET.get('menu')
    perspective = Perspective.objects.none()
    department = Department.objects.get(department=request.user.department)
    get_perspectives = Perspective.objects.all()#these are the listed perspectives
    user_first_last_name = request.user.first_name + ' ' + request.user.last_name
    
    if initialTemplate:
        department_template_exists_in_initial_template = InitialTemplateDetail.objects.filter(department=department, template_Name=initialTemplate.template_Name).first()
        if not department_template_exists_in_initial_template:
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    
    departmental_objectives_per_perspective = DepartmentalObjective.objects.none()
    departmentalObjectives = DepartmentalObjective.objects.none()
    
    if request.GET.get('perspective'):
        perspective = Perspective.objects.get(perspective=request.GET.get('perspective'))
        if not department_template_exists_in_initial_template:
            departmental_objectives_per_perspective = DepartmentalObjective.objects.none()
        else:
            departmental_objectives_per_perspective = DepartmentalObjective.objects.filter(department=department, perspective=perspective.id, template_name=department_template_exists_in_initial_template.id)
    else:
        if not department_template_exists_in_initial_template:
            departmentalObjectives = DepartmentalObjective.objects.none()
        else:
            departmentalObjectives = DepartmentalObjective.objects.filter(department=department, template_name=department_template_exists_in_initial_template.id)
            
    deliverables = Deliverable.objects.filter(lead_person=user_first_last_name)
    activities = DepartmentalInitiativeOrActivities.objects.all()
    performance_measures = PerformanceMeasure.objects.all()
    strategic_results = StrategicResult.objects.all()
    
    deliverables_count = []
    activities_count = []
    objectives_count = []
    
    manager_department_statistics = statistical_data(departmentalObjectives, strategic_results, performance_measures, activities, deliverables)
    manager_department_statistics_per_perspective = statistical_data(departmental_objectives_per_perspective, strategic_results, performance_measures, activities, deliverables)
    print(manager_department_statistics)
    print(request.GET.get('perspective'), manager_department_statistics_per_perspective)
    
    
    if not deliverables:
        deliverables = Deliverable.objects.none()
    else:
        for deliverable in deliverables:
            deliverables_count.append(deliverable)
            for activity in activities:
                if deliverable.departmentalInitiativeOrActivity == activity:
                    activities_count.append(activity)
                    for performance_measure in performance_measures:
                        if performance_measure == activity.performance_measure:
                            for strategic_result in strategic_results:
                                if strategic_result == performance_measure.strategic_result:
                                    if request.GET.get('perspective'):
                                        for departmental_objective_per_perspective in departmental_objectives_per_perspective:
                                            if strategic_result.departmental_objective == departmental_objective_per_perspective:
                                                objectives_count.append(departmental_objective_per_perspective)
                                    else:
                                        for departmentalObjective in departmentalObjectives:
                                            if strategic_result.departmental_objective == departmentalObjective:
                                                objectives_count.append(departmentalObjective)

    
    context = {
        'menu': menu,
        'perspectives': get_perspectives,
        'initialTemplate': initialTemplate,
        'department_template_exists_in_initial_template': department_template_exists_in_initial_template,
        'manager_department_statistics': manager_department_statistics,
        'manager_department_statistics_per_perspective': manager_department_statistics_per_perspective,
    }
    
    return render(request, 'managerDashboard.html', context)

@login_required(login_url='userLogin')
def awp(request):
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    print(initialTemplate)
    perspectives = Perspective.objects.all()
    department = Department.objects.get(department=request.user.department)
    menu = request.GET.get('menu')
    
    if initialTemplate:
        department_template_exists_in_initial_template = InitialTemplateDetail.objects.filter(department=department, template_Name=initialTemplate.template_Name).first()
        print('Department Template: ',department_template_exists_in_initial_template)
        if not department_template_exists_in_initial_template:
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()

    get_departmentalObjectives = DepartmentalObjective.objects.filter(department=department)
    get_strategicResuts = StrategicResult.objects.all()
    get_performanceMeasures = PerformanceMeasure.objects.all()
    get_targets = Target.objects.all()
    getDepartmentalInitiatives = DepartmentalInitiativeOrActivities.objects.all()
    getDeliverables = Deliverable.objects.all()
    
    context = {
        'initialTemplate': initialTemplate,
        'department_template_exists_in_initial_template': department_template_exists_in_initial_template,
        'menu': menu, 
        'perspectives': perspectives,
        'departmentalObjectives': get_departmentalObjectives,
        'strategicResults': get_strategicResuts,
        'performanceMeasures': get_performanceMeasures,
        'targets_quarterly_annual': get_targets,
        'departmentalInitiatives': getDepartmentalInitiatives,
        'deliverables': getDeliverables,
    }
    return render(request, 'awp.html', context)

def scoreCardFunction(request, templateName, url_name):
    # TEMPLATES 
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    print(initialTemplate)
    get_perspective = request.GET.get('perspective')
    get_menu = request.GET.get('menu')
    get_section = request.GET.get('section')
    section = request.GET.get('section')
    perspective = Perspective.objects.get(perspective=get_perspective)
    department = Department.objects.get(department=request.user.department)
    
    if initialTemplate:
        department_template_exists_in_initial_template = InitialTemplateDetail.objects.filter(department=department, template_Name=initialTemplate.template_Name).first()
        print(department_template_exists_in_initial_template)
        if not department_template_exists_in_initial_template:
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    
    departmentalObjectiveForm = DepartmentalObjectiveForm()
    strategicResultForm = StrategicResultForm()
    performanceMeasureForm = PerformanceMeasureForm()
    targetsForm = TargetsForm()
    formularForm = FormulaForm()
    performanceMeasureActualResultsForm = PerformanceMeasureActualResultsForm()
    departmentalInitiativeOrActivitiesForm = DepartmentalInitiativeOrActivitiesForm()
    deliverablesForm = DeliverableForm()
    actualExpenditureForm = ActualExpenditureForm()

    if request.method == 'POST':

        if request.POST.get('departmentalObjectiveBtn') == 'departmentalObjective':
            departmentalObjectiveForm = DepartmentalObjectiveForm(request.POST)

            if departmentalObjectiveForm.is_valid():

                departmentalObjectiveFormInstance = departmentalObjectiveForm.save(commit=False)
                departmentalObjectiveFormInstance.perspective = perspective
                departmentalObjectiveFormInstance.department = department
                departmentalObjectiveFormInstance.template_name = InitialTemplateDetail.objects.get(id=department_template_exists_in_initial_template.id)
                departmentalObjectiveFormInstance.financial_year = str(department_template_exists_in_initial_template.financial_Year_Starts) + '-' + str(department_template_exists_in_initial_template.financial_Year_Ends)

                departmentalObjectiveFormInstance.save()

                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)
        elif request.POST.get('strategicResultBtn') == 'strategicResult':
            strategicResultForm = StrategicResultForm(request.POST)

            departmentalObjective = DepartmentalObjective.objects.get(id=request.POST.get('departmentalObjective'))

            if strategicResultForm.is_valid():
                strategicResultFormInstance = strategicResultForm.save(commit=False)
                strategicResultFormInstance.departmental_objective = departmentalObjective

                strategicResultFormInstance.save()

                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)
        elif request.POST.get('performanceMeasureBtn') == 'performanceMeasure':
            performanceMeasureForm = PerformanceMeasureForm(request.POST)
            strategicResult = StrategicResult.objects.get(id=request.POST.get('strategicResult'))

            if performanceMeasureForm.is_valid():
                performanceMeasureFormInstance = performanceMeasureForm.save(commit=False)
                performanceMeasureFormInstance.strategic_result = strategicResult

                performanceMeasureFormInstance.save()

                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)
        # WORK PLAN SECTION
        elif request.POST.get('departmentalInitiativeBtn') == 'departmentalInitiative':
            departmentalInitiativeOrActivitiesForm = DepartmentalInitiativeOrActivitiesForm(request.POST)
            performanceMeasure = PerformanceMeasure.objects.get(id=request.POST.get('performanceMeasure'))

            if departmentalInitiativeOrActivitiesForm.is_valid():
                departmentalInitiativeOrActivitiesFormInstance = departmentalInitiativeOrActivitiesForm.save(commit=False)
                departmentalInitiativeOrActivitiesFormInstance.performance_measure = performanceMeasure

                departmentalInitiativeOrActivitiesFormInstance.save()
                
                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)
        elif request.POST.get('deliverablesBtn') == 'deliverables':
            deliverablesForm = DeliverableForm(request.POST)
            departmentalInitiative = DepartmentalInitiativeOrActivities.objects.get(id=request.POST.get('departmentalInitiativeOrActivity'))
            lead_person = request.POST.get('lead_person')
            deliverable_to_be_saved = request.POST.get('deliverable')
            
            if deliverablesForm.is_valid():
                deliverableFormInstance = deliverablesForm.save(commit=False)
                deliverableFormInstance.departmentalInitiativeOrActivity = departmentalInitiative
                deliverableFormInstance.lead_person = lead_person
                deliverableFormInstance.save()
                
                # find if deliverable is saved
                deliverable_saved = Deliverable.objects.get(deliverable=deliverable_to_be_saved)
                if deliverable_saved.lead_person != 'Not Assigned':
                    deliverable_saved.deliverable_status = 'In progress'
                    
                    deliverable_saved.save()
                else:
                    print('Deliverable status not changed')

                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)
        elif request.POST.get('actualExpenditureBtn') == 'actualExpenditure':
            actualExpenditureForm = ActualExpenditureForm(request.POST)
            departmentalInitiative = DepartmentalInitiativeOrActivities.objects.get(id=request.POST.get('departmentalInitiativeOrActivity'))

            if actualExpenditureForm.is_valid():
                actualExpenditureFormInstance = actualExpenditureForm.save(commit=False)
                actualExpenditureFormInstance.departmentalInitiativeOrActivity = departmentalInitiative

                actualExpenditureFormInstance.save()

                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&item=par' +'&menu=' + get_menu + '&section=' + get_section)
        
        # UPDATE DEPARTMENT ACTIVITIES IN THE AWP SECTION
        elif request.POST.get('departmentalInitiativeOrActivityUpdateBtn') == 'departmentalInitiativeOrActivityUpdate':
            departmentalInitiativeOrActivity = DepartmentalInitiativeOrActivities.objects.get(id=request.POST.get('departmentalInitiativeOrActivity'))
            departmentalInitiativeOrActivitiesForm = DepartmentalInitiativeOrActivitiesForm(request.POST, instance=departmentalInitiativeOrActivity)
            
            if departmentalInitiativeOrActivitiesForm.is_valid():
                departmentalInitiativeOrActivitiesForm.save()
                return redirect(reverse(url_name) + '?perspective=' + perspective + '&section=' + section + '&menu=' + get_menu )

        # UPDATE DELIVERABLES
        elif request.POST.get('deliverableUpdateBtn') == 'deliverableUpdate':
            deliverable = Deliverable.objects.get(id=request.POST.get('deliverable_id'))
            deliverablesForm = DeliverableForm(request.POST, instance=deliverable)
            # deliverablesForm.lead_person = request.POST.get('lead_person')
            lead_person = request.POST.get('lead_person')
            # deliverablesForm = DeliverableForm(request.POST, instance=deliverable) 

            if deliverablesForm.is_valid():
                formInstance = deliverablesForm.save(commit=False)
                formInstance.lead_person = lead_person
                formInstance.save()
                # deliverableFormInstance.save()

                return redirect(reverse(url_name) + '?perspective=' + perspective + '&section=' + section + '&menu=' + get_menu )
            else:
                print('Form invalid')
        # UPDATE ACTUAL EXPENDITURE
        elif request.POST.get('actualExpenditureUpdateBtn') =='actualExpenditureUpdate':
            actualExpenditure = ActualExpenditure.objects.get(id=request.POST.get('actualExpenditure_id'))
            actualExpendituresForm = ActualExpenditureForm(request.POST,instance=actualExpenditure)

            if actualExpendituresForm.is_valid():
                actualExpendituresForm.save()
                return redirect(reverse(url_name) + '?perspective=' + perspective + '&item=par' +'&menu=' + get_menu + '&section=' + section)
        elif request.POST.get('targetsQuarterlyAnnualBtn') == 'targetsQuarterlyAnnual':
            targetsForm = TargetsForm(request.POST)
            performanceMeasure = PerformanceMeasure.objects.get(id=request.POST.get('performanceMeasure'))
            
            if targetsForm.is_valid():
                targetsFormInstance = targetsForm.save(commit=False)
                targetsFormInstance.performance_measure = performanceMeasure
                targetsFormInstance.save()

                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)
        elif request.POST.get('formulaBtn') == 'formula':
            formulaForm = FormulaForm(request.POST)
            performanceMeasure = PerformanceMeasure.objects.get(id=request.POST.get('performanceMeasure'))

            if formulaForm.is_valid():
                formulaFormInstance = formulaForm.save(commit=False)
                formulaFormInstance.performance_measure = performanceMeasure

                formulaFormInstance.save()
                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&item=par' +'&menu=' + get_menu + '&section=' + get_section)
        elif request.POST.get('performanceMeasureActualResultsBtn') == 'performanceMeasureActualResults':
            performanceMeasureActualResultsForm = PerformanceMeasureActualResultsForm(request.POST)
            formula = Formula.objects.get(id=request.POST.get('formula'))

            if performanceMeasureActualResultsForm.is_valid():
                performanceMeasureActualResultsFormInstance = performanceMeasureActualResultsForm.save(commit=False)
                performanceMeasureActualResultsFormInstance.formula = formula

                performanceMeasureActualResultsFormInstance.save()
                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&item=par' +'&menu=' + get_menu + '&section=' + get_section)
        # UPDATE DEPARTMENTAL OBJECTIVES SECTION
        elif request.POST.get('departmentalObjectiveUpdateBtn') == 'departmentalObjectiveUpdate':
            departmentalObjective = DepartmentalObjective.objects.get(id=request.POST.get('objective_update_id'))
            departmentalObjectiveForm = DepartmentalObjectiveForm(request.POST, instance=departmentalObjective)

            if departmentalObjectiveForm.is_valid():
                departmentalObjectiveForm.save()
                
                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)
        # UPDATE STRATEGIC RESULT
        elif request.POST.get('updateStrategicResultBtn')  == 'updateStrategicResult':
            strategicResult = StrategicResult.objects.get(id=request.POST.get('strategic_update_id'))
            strategicResultForm =StrategicResultForm(request.POST, instance=strategicResult)

            if strategicResultForm.is_valid():
                strategicResultForm.save()

                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)
        # UPDATE PERFOMANCE MEASURE
        elif request.POST.get('performanceMeasureUpdateBtn') == 'performanceMeasureUpdate':
            performanceMeasure = PerformanceMeasure.objects.get(id=request.POST.get('performanceMeasure_update_id'))
            performanceMeasureForm = PerformanceMeasureForm(request.POST, instance=performanceMeasure)

            if performanceMeasureForm.is_valid():
                performanceMeasureForm.save()
                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)

        # UPDATE TARGETS
        elif request.POST.get('targetUpdateBtn') == 'targetUpdate':
            target = Target.objects.get(id=request.POST.get('target_quarterly_annual_update_id'))
            targetsForm =TargetsForm(request.POST,instance=target)

            if targetsForm.is_valid():
                targetsForm.save()
                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&menu=' + get_menu + '&section=' + get_section)

        # UPDATE FORMULA
        elif request.POST.get('formulaUpdateBtn') == 'formulaUpdate':
            formula = Formula.objects.get(id=request.POST.get('formula_update_id'))
            formulaForm = FormulaForm(request.POST,instance=formula)

            if formulaForm.is_valid():
                formulaForm.save()
                return redirect(reverse(url_name) + '?perspective=' + get_perspective + '&item=par' +'&menu=' + get_menu + '&section=' + get_section)


    # NO TEMPLATE
    get_current_template_objectives = DepartmentalObjective.objects.none()
     
    # TEMPLATE EXISTS
    if department_template_exists_in_initial_template:
        get_current_template_objectives = DepartmentalObjective.objects.filter(department=department, perspective=perspective, template_name=department_template_exists_in_initial_template.id)
    get_last_Objective = get_current_template_objectives.last()
    print(get_current_template_objectives)

    get_strategicResuts = StrategicResult.objects.all()
    get_performanceMeasures = PerformanceMeasure.objects.all()
    get_targets = Target.objects.all()
    get_formula = Formula.objects.all()
    get_performanceMeasuresActualResults = PerformanceMeasureActualResults.objects.all()
    getDepartmentalInitiatives = DepartmentalInitiativeOrActivities.objects.all()
    getDeliverables = Deliverable.objects.all()
    department_users_list = []
    getDepartmentUsers = CustomUserRegistration.objects.filter(department=request.user.department)
    
    getActualExpenditure = ActualExpenditure.objects.all()
    achievements = AchievementChallenge.objects.all()
    
    for department_user in getDepartmentUsers:
        if department_user.first_name + ' ' + department_user.last_name not in department_users_list:
            department_users_list.append(department_user.first_name + ' ' + department_user.last_name)
    

    context = {
        'initialTemplate': initialTemplate,
        'department_template_exists_in_initial_template': department_template_exists_in_initial_template,
        'perspective': get_perspective,
        'perspective_id': perspective, 
        'section': get_section, 
        'menu': get_menu,
        'form': departmentalObjectiveForm,
        'departmentalObjectives': get_current_template_objectives,
        'strategicResultForm': strategicResultForm,
        'strategicResults': get_strategicResuts,
        'performanceMeasureForm': performanceMeasureForm,
        'performanceMeasures': get_performanceMeasures,
        'last_objective': get_last_Objective,
        'targetsForm': targetsForm,
        'targets_quarterly_annual': get_targets,
        'formulaForm': formularForm,
        'formulas': get_formula,
        'performanceMeasuresActualResultsForm': performanceMeasureActualResultsForm,
        'performanceMeasuresActualResults': get_performanceMeasuresActualResults,
        'departmentalActivitiesForm': departmentalInitiativeOrActivitiesForm,
        'departmentalInitiativesOrActivities': getDepartmentalInitiatives,
        'deliverablesForm': deliverablesForm,
        'deliverables': getDeliverables,
        'departmentUsers': department_users_list,
        'actualExpenditureForm': actualExpenditureForm,
        'actualExpenditures': getActualExpenditure,
        'achievements_challenges': achievements,
    }
    return render(request, templateName, context)

def awp_wp_func(request, templateName, url_name):
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    section = request.GET.get('section')
    perspective = request.GET.get('perspective')
    department = request.user.department
    getPerspective = Perspective.objects.get(perspective=perspective)
    getDepartment = Department.objects.get(department=department)
    
    if initialTemplate:
        department_template_exists_in_initial_template = InitialTemplateDetail.objects.filter(department=department, template_Name=initialTemplate.template_Name).first()
        print(department_template_exists_in_initial_template)
        if not department_template_exists_in_initial_template:
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
            

    get_menu = request.GET.get('menu')

    #forms
    departmentalInitiativeOrActivitiesForm = DepartmentalInitiativeOrActivitiesForm()
    deliverablesForm = DeliverableForm()
    actualExpenditureForm = ActualExpenditureForm()

     # NO TEMPLATE
    get_current_template_objectives = DepartmentalObjective.objects.none()
     
    # TEMPLATE EXISTS
    if department_template_exists_in_initial_template:
        get_current_template_objectives = DepartmentalObjective.objects.filter(department=department, perspective=getPerspective, template_name=department_template_exists_in_initial_template.id)
    # get_last_Objective = get_current_template_objectives.last()
    print(get_current_template_objectives)
    strategicResults = StrategicResult.objects.all()
    performanceMeasures = PerformanceMeasure.objects.all()
    

    if request.method == 'POST':

        if request.POST.get('departmentalInitiativeBtn') == 'departmentalInitiative':
            departmentalInitiativeOrActivitiesForm = DepartmentalInitiativeOrActivitiesForm(request.POST)
            performanceMeasure = PerformanceMeasure.objects.get(id=request.POST.get('performanceMeasure'))

            if departmentalInitiativeOrActivitiesForm.is_valid():
                departmentalInitiativeOrActivitiesFormInstance = departmentalInitiativeOrActivitiesForm.save(commit=False)
                departmentalInitiativeOrActivitiesFormInstance.performance_measure = performanceMeasure

                departmentalInitiativeOrActivitiesFormInstance.save()

                return redirect(reverse(url_name) + '?perspective=' + perspective + '&section=' + section + '&menu=' + get_menu )
        elif request.POST.get('deliverablesBtn') == 'deliverables':
            deliverablesForm = DeliverableForm(request.POST)
            departmentalInitiative = DepartmentalInitiativeOrActivities.objects.get(id=request.POST.get('departmentalInitiativeOrActivity'))
            lead_person = request.POST.get('lead_person')
            deliverable_to_be_saved = request.POST.get('deliverable')
            
            if deliverablesForm.is_valid():
                deliverableFormInstance = deliverablesForm.save(commit=False)
                deliverableFormInstance.departmentalInitiativeOrActivity = departmentalInitiative
                deliverableFormInstance.lead_person = lead_person
                deliverableFormInstance.save()
                
                # find if deliverable is saved
                deliverable_saved = Deliverable.objects.get(deliverable=deliverable_to_be_saved)
                if deliverable_saved.lead_person != 'Not Assigned':
                    deliverable_saved.deliverable_status = 'In progress'
                    
                    deliverable_saved.save()
                else:
                    print('Deliverable status not changed')

                return redirect(reverse(url_name) + '?perspective=' + perspective + '&section=' + section + '&menu=' + get_menu )
        elif request.POST.get('actualExpenditureBtn') == 'actualExpenditure':
            actualExpenditureForm = ActualExpenditureForm(request.POST)
            departmentalInitiative = DepartmentalInitiativeOrActivities.objects.get(id=request.POST.get('departmentalInitiativeOrActivity'))

            if actualExpenditureForm.is_valid():
                actualExpenditureFormInstance = actualExpenditureForm.save(commit=False)
                actualExpenditureFormInstance.departmentalInitiativeOrActivity = departmentalInitiative

                actualExpenditureFormInstance.save()

                return redirect(reverse(url_name) + '?perspective=' + perspective + '&item=par' +'&menu=' + get_menu + '&section=' + section)
        
        # UPDATE DEPARTMENT ACTIVITIES IN THE AWP SECTION
        elif request.POST.get('departmentalInitiativeOrActivityUpdateBtn') == 'departmentalInitiativeOrActivityUpdate':
            departmentalInitiativeOrActivity = DepartmentalInitiativeOrActivities.objects.get(id=request.POST.get('departmentalInitiativeOrActivity'))
            departmentalInitiativeOrActivitiesForm = DepartmentalInitiativeOrActivitiesForm(request.POST, instance=departmentalInitiativeOrActivity)
            
            if departmentalInitiativeOrActivitiesForm.is_valid():
                departmentalInitiativeOrActivitiesForm.save()
                return redirect(reverse(url_name) + '?perspective=' + perspective + '&section=' + section + '&menu=' + get_menu )

        # UPDATE DELIVERABLES
        elif request.POST.get('deliverableUpdateBtn') == 'deliverableUpdate':
            deliverable = Deliverable.objects.get(id=request.POST.get('deliverable_id'))
            deliverablesForm = DeliverableForm(request.POST, instance=deliverable)
            # deliverablesForm.lead_person = request.POST.get('lead_person')
            lead_person = request.POST.get('lead_person')
            # deliverablesForm = DeliverableForm(request.POST, instance=deliverable) 

            if deliverablesForm.is_valid():
                formInstance = deliverablesForm.save(commit=False)
                formInstance.lead_person = lead_person
                formInstance.save()
                # deliverableFormInstance.save()

                return redirect(reverse(url_name) + '?perspective=' + perspective + '&section=' + section + '&menu=' + get_menu )
            else:
                print('Form invalid')
        # UPDATE ACTUAL EXPENDITURE
        elif request.POST.get('actualExpenditureUpdateBtn') =='actualExpenditureUpdate':
            actualExpenditure = ActualExpenditure.objects.get(id=request.POST.get('actualExpenditure_id'))
            actualExpendituresForm = ActualExpenditureForm(request.POST,instance=actualExpenditure)

            if actualExpendituresForm.is_valid():
                actualExpendituresForm.save()
                return redirect(reverse(url_name) + '?perspective=' + perspective + '&item=par' +'&menu=' + get_menu + '&section=' + section)

    getDepartmentalInitiatives = DepartmentalInitiativeOrActivities.objects.all()
    getDeliverables = Deliverable.objects.all()
    department_users_list = []
    getDepartmentUsers = CustomUserRegistration.objects.filter(department=request.user.department)
    for department_user in getDepartmentUsers:
        if department_user.first_name + ' ' + department_user.last_name not in department_users_list:
            department_users_list.append(department_user.first_name + ' ' + department_user.last_name)
    
    getActualExpenditure = ActualExpenditure.objects.all()
    
    achievements = AchievementChallenge.objects.all()
    print('These are the achievements and challenges: ', achievements)

    context = {
        'initialTemplate': initialTemplate,
        'department_template_exists_in_initial_template': department_template_exists_in_initial_template,
        'perspective': perspective,
        'section': section, 
        'menu': get_menu,
        'departmentalObjectives': get_current_template_objectives,
        'strategicResults': strategicResults,
        'performanceMeasures': performanceMeasures,
        'departmentalActivitiesForm': departmentalInitiativeOrActivitiesForm,
        'departmentalInitiativesOrActivities': getDepartmentalInitiatives,
        'deliverablesForm': deliverablesForm,
        'deliverables': getDeliverables,
        'departmentUsers': department_users_list,
        'actualExpenditureForm': actualExpenditureForm,
        'actualExpenditures': getActualExpenditure,
        'achievements_challenges': achievements,
    }
    return render(request, templateName, context)

@login_required(login_url='userLogin')
def awp_sc_Customer(request):
    # the function needs a url
    return scoreCardFunction(request,'awp_sc_Customer.html', 'awp_sc_Customer')

@login_required(login_url='userLogin')
def awp_sc_Finance(request):
    return scoreCardFunction(request, 'awp_sc_Finance.html', 'awp_sc_Finance')

    # return render(request, 'awp_sc_Finance.html', context)

@login_required(login_url='userLogin')
def awp_sc_InternalBusinessProcesses(request):
    return scoreCardFunction(request, 'awp_sc_InternalBusinessProcesses.html', 'awp_sc_InternalBusinessProcesses')
    # return render(request, 'awp_sc_InternalBusinessProcesses.html', context)

@login_required(login_url='userLogin')
def awp_sc_OrganizationalCapacity(request):
    return scoreCardFunction(request, 'awp_sc_OrganizationalCapacity.html', 'awp_sc_OrganizationalCapacity')
    # return render(request, 'awp_sc_OrganizationalCapacity.html', context)

@login_required(login_url='userLogin')
def awp_wp_Customer(request):
    return awp_wp_func(request, 'awp_wp_Customer.html', 'awp_wp_Customer')

@login_required(login_url='userLogin')
def awp_wp_Finance(request):
    return awp_wp_func(request, 'awp_wp_Finance.html', 'awp_wp_Finance')

@login_required(login_url='userLogin')
def awp_wp_InternalBusinessProcesses(request):
    return awp_wp_func(request, 'awp_wp_InternalBusinessProcesses.html', 'awp_wp_InternalBusinessProcesses')

@login_required(login_url='userLogin')
def awp_wp_OrganizationalCapacity(request):
    return awp_wp_func(request, 'awp_wp_OrganizationalCapacity.html', 'awp_wp_OrganizationalCapacity')

def par(request):
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    print(initialTemplate)
    perspectives = Perspective.objects.all()
    department = Department.objects.get(department=request.user.department)
    menu = request.GET.get('menu')
    
    if initialTemplate:
        department_template_exists_in_initial_template = InitialTemplateDetail.objects.filter(department=department, template_Name=initialTemplate.template_Name).first()
        print('Department Template: ',department_template_exists_in_initial_template)
        if not department_template_exists_in_initial_template:
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    
    get_departmentalObjectives = DepartmentalObjective.objects.filter(department=department)
    get_strategicResuts = StrategicResult.objects.all()
    get_performanceMeasures = PerformanceMeasure.objects.all()
    get_targets = Target.objects.all()
    getDepartmentalInitiatives = DepartmentalInitiativeOrActivities.objects.all()
    getDeliverables = Deliverable.objects.all()
    formulas = Formula.objects.all()
    
    context = {
        'menu': menu,
        'initialTemplate': initialTemplate,
        'department_template_exists_in_initial_template': department_template_exists_in_initial_template,
        'perspectives': perspectives,
        'departmentalObjectives': get_departmentalObjectives,
        'strategicResults': get_strategicResuts, 
        'performanceMeasures': get_performanceMeasures,
        'targets_quarterly_annual': get_targets,
        'departmentalInitiatives': getDepartmentalInitiatives,
        'deliverables': getDeliverables,
        'formulas': formulas
    }
    return render(request, 'par/par.html', context)

def par_sc_Customer(request):
    return scoreCardFunction(request,'par/par_sc_Customer.html', 'par_sc_Customer')

def par_sc_Finance(request):
    return scoreCardFunction(request,'par/par_sc_Finance.html', 'par_sc_Customer')


def par_sc_InternalBusinessProcesses(request):
    return scoreCardFunction(request,'par/par_sc_InternalBusinessProcesses.html', 'par_sc_Customer')

def par_sc_OrganizationalCapacity(request):
    return scoreCardFunction(request,'par/par_sc_OrganizationalCapacity.html', 'par_sc_Customer')

def par_wp_Customer(request):
    return awp_wp_func(request, 'par/par_wp_Customer.html', 'par_wp_Customer')

def par_wp_Finance(request):
    return awp_wp_func(request, 'par/par_wp_Finance.html', 'par_wp_Finance')

def par_wp_InternalBusinessProcesses(request):
    return awp_wp_func(request, 'par/par_wp_InternalBusinessProcesses.html', 'par_wp_InternalBusinessProcesses')

def par_wp_OrganizationalCapacity(request):
    return awp_wp_func(request, 'par/par_wp_OrganizationalCapacity.html', 'par_wp_OrganizationalCapacity')


def my_par_perspectives_func(request, templateName, template_url):
    achievementChallengeForm = AchievementChallengeForm()
    menu = request.GET.get('menu')
    perspective = request.GET.get('perspective')
    if not perspective:
        getPerspective = Perspective.objects.none()
    else:
        getPerspective = Perspective.objects.get(perspective=perspective)
    user_first_last_name = request.user.first_name + ' ' + request.user.last_name
    
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    department = Department.objects.get(department=request.user.department)

    if initialTemplate:
        department_template_exists_in_initial_template = InitialTemplateDetail.objects.filter(department=department, template_Name=initialTemplate.template_Name).first()
        if not department_template_exists_in_initial_template:
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    
    # NO TEMPLATE
    get_current_template_objectives = DepartmentalObjective.objects.none()
     
    # TEMPLATE EXISTS
    if department_template_exists_in_initial_template:
        # Not based on the perspective
        if request.GET.get('category'):
            get_current_template_objectives = DepartmentalObjective.objects.filter(department=department, template_name=department_template_exists_in_initial_template.id)
        else:    
            get_current_template_objectives = DepartmentalObjective.objects.filter(department=department, perspective=getPerspective, template_name=department_template_exists_in_initial_template.id)

    print(get_current_template_objectives)

    if request.method == 'POST':

        if request.POST.get('achievementBtn') == 'achievement':
            achievementChallengeForm = AchievementChallengeForm(request.POST)
            deliverable = Deliverable.objects.get(id=request.POST.get('deliverable'))

            if achievementChallengeForm.is_valid():
                achievementFormInstance = achievementChallengeForm.save(commit=False)
                achievementFormInstance.deliverable = deliverable
                achievementFormInstance.achievement_status = 'Done'
                achievementFormInstance.save()
                
                # find achievement with this deliverable id
                saved_achievement = AchievementChallenge.objects.get(deliverable=deliverable.id)
                # check if its status is done
                if saved_achievement.achievement_status == 'Done':
                    # change the deliverable status to done
                    deliverable.deliverable_status = 'Done'
                    deliverable.save()
                else:
                    print('Deliverable Status not changed')

                return redirect(reverse(template_url) + '?perspective=' + perspective + '&menu=' + menu)
            else:
                print('form is invalid')
        # ACHIEVEMENT AND CHALLENGES UPDATE FUNCTIONALITY
        elif request.POST.get('achievemenUpdateBtn') == "achievemenUpdate":
            achievement = AchievementChallenge.objects.get(id=request.POST.get('achievement_update_id')) 
            achievementChallengeForm = AchievementChallengeForm(request.POST, instance=achievement)  

            if achievementChallengeForm.is_valid():
                achievementChallengeForm.save()
                return redirect(reverse(template_url) + '?perspective=' + perspective + '&menu=' + menu)
            else:
                print('YOU MF')

    # Get Deliverables
    deliverables = Deliverable.objects.filter(lead_person=user_first_last_name)
    users_assigned_deliverables_list = []
    
    
    for departmental_objective in get_current_template_objectives:
        for strategic_result in StrategicResult.objects.all():
            if strategic_result.departmental_objective == departmental_objective:
                for performance_measure in PerformanceMeasure.objects.all():
                    if performance_measure.strategic_result == strategic_result:
                        # departmental_activities = DepartmentalInitiativeOrActivities.objects.filter(performance_measure=PerformanceMeasure.objects.get(performance_measure=performance_measure).id)
                        # print(departmental_activities)
                        for departmental_activity in DepartmentalInitiativeOrActivities.objects.all():
                            if departmental_activity.performance_measure == performance_measure:
                                for deliverable in Deliverable.objects.all():
                                    if deliverable.departmentalInitiativeOrActivity == departmental_activity and deliverable.lead_person == user_first_last_name:
                                        users_assigned_deliverables_list.append(deliverable.lead_person)

    for deliverable in deliverables:
        if deliverable.lead_person not in users_assigned_deliverables_list:
            users_assigned_deliverables_list.append(deliverable.lead_person)
    
    # print(users_assigned_deliverables_list)
    get_achievements = AchievementChallenge.objects.all()
    all_perspectives = Perspective.objects.all()
    # print('These are the achievements: ', get_achievements)

    context = {
        'menu': menu,
        'perspective': request.GET.get('perspective'),
        'deliverables': deliverables,
        'initialTemplate': initialTemplate,
        'department_template_exists': department_template_exists_in_initial_template,
        'departmentalObjectives': get_current_template_objectives,
        'strategicResults': StrategicResult.objects.all(),
        'performanceMeasures': PerformanceMeasure.objects.all(),
        'departmentalActivities': DepartmentalInitiativeOrActivities.objects.all(),
        'deliverables': Deliverable.objects.all(),
        'user': user_first_last_name,
        'user_with_deliverables': users_assigned_deliverables_list,
        'achievementChallengeForm': achievementChallengeForm,
        'achievementsChallenges': get_achievements,
        'departmentPerspectives': all_perspectives,
    }

    return render(request, templateName, context)

# My Par views
def my_par(request):
    return my_par_perspectives_func(request, 'mypar/mypar.html', 'my_par')    

def my_par_customer(request):
    return my_par_perspectives_func(request, 'mypar/my_par_wp_Customer.html', 'my_par_customer')

def my_par_finance(request):
    return my_par_perspectives_func(request, 'mypar/my_par_wp_Finance.html', 'my_par_finance')

def my_par_internal_business_processes(request):
    return my_par_perspectives_func(request, 'mypar/my_par_wp_Internal_Business_Processes.html', 'my_par_internal_business_processes')

def my_par_organizational_capacity(request):
    return my_par_perspectives_func(request, 'mypar/my_par_wp_Organizational_Capacity.html', 'my_par_organizational_capacity')


# DEPARTMENTS AWP
def departments_awp(request):
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    perspectives = Perspective.objects.all()
    menu = request.GET.get('menu')
    all_departments = Department.objects.all()
    specific_department = Department.objects.none()
    department_objectives = DepartmentalObjective.objects.all()
    
    if request.GET.get('department'):
        specific_department = Department.objects.get(department=request.GET.get('department'))
        department_objectives = DepartmentalObjective.objects.filter(department=specific_department)
        
    perspectives_in_objectives_list = []
    
    if initialTemplate:
        if request.GET.get('department'):
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.filter(department=specific_department, template_Name=initialTemplate.template_Name).first()
        if not department_template_exists_in_initial_template:
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    
    strategic_results = StrategicResult.objects.all()
    performance_measures = PerformanceMeasure.objects.all()
    departmental_initiatives = DepartmentalInitiativeOrActivities.objects.all()
    deliverables = Deliverable.objects.all()
    
    for department_objective in department_objectives:
        for perspective in perspectives:
            if perspective == department_objective.perspective:
                if department_objective.perspective not in perspectives_in_objectives_list:
                    perspectives_in_objectives_list.append(department_objective.perspective)
   
    context = {
        'menu': menu,
        'department_template_exists_in_initial_template': department_template_exists_in_initial_template,
        'departments': all_departments,
        'department': specific_department,
        'perspectives': perspectives,
        'perspectives_in_objectives_list': perspectives_in_objectives_list,
        'departmental_objectives': department_objectives,
        'strategic_results': strategic_results,
        'performance_measures': performance_measures,
        'departmental_initiatives': departmental_initiatives,
        'deliverables': deliverables,
        'initialTemplate': initialTemplate,
        
    }
    return render(request, 'strategy/departments_awp.html', context)

def departments_par(request):
    menu = request.GET.get('menu')
    item = request.GET.get('item')
    initialTemplate = InitialTemplateDetail.objects.filter(template_Status='open', user_is_strategy=True).first()
    department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    perspectives = Perspective.objects.all()
    all_departments = Department.objects.all()
    specific_department = Department.objects.none()
    department_objectives = DepartmentalObjective.objects.all()
    
    if request.GET.get('department'):
        specific_department = Department.objects.get(department=request.GET.get('department'))
        department_objectives = DepartmentalObjective.objects.filter(department=specific_department)
    
    
    
    perspectives_in_objectives_list = []
    
    if initialTemplate:
        if request.GET.get('department'):
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.filter(department=specific_department, template_Name=initialTemplate.template_Name).first()
        if not department_template_exists_in_initial_template:
            department_template_exists_in_initial_template = InitialTemplateDetail.objects.none()
    
    strategic_results = StrategicResult.objects.all()
    performance_measures = PerformanceMeasure.objects.all()
    departmental_initiatives = DepartmentalInitiativeOrActivities.objects.all()
    deliverables = Deliverable.objects.all()
    formula = Formula.objects.all()
    actual_expenditures = ActualExpenditure.objects.all()
    achievements_challenges = AchievementChallenge.objects.all()
    
    for department_objective in department_objectives:
        for perspective in perspectives:
            if perspective == department_objective.perspective:
                if department_objective.perspective not in perspectives_in_objectives_list:
                    perspectives_in_objectives_list.append(department_objective.perspective)
                    
    for departmentalObjective in department_objectives:
        print('Another Ob', departmentalObjective)
        for strategicResult in strategic_results:
            if departmentalObjective == strategicResult.departmental_objective:
                print('Another Strategic', departmentalObjective)
                for performance_measure in performance_measures:
                    if performance_measure.strategic_result == strategicResult:
                        print('This is the performance measure', performance_measure)
                        # print('Another Full Print', request.GET.get('department'), performance_measure.id, performance_measure)
                    
    def download_file_as_excel():
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="par_quarters.xls"'
        wb = xlwt.Workbook()
        ws = wb.add_sheet('QuarterlyPar')
        
        # sheet header first row
        row_num = 0
        # columns = ['Department', 'Department_ID','Measure', 'Quarter_1(30-06)', 'Quarter_2(30-09)', 'Quarter_3(31-12)', 'Quarter_4(31-03)']
        columns = ['Department', 'Department_ID','Measure']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for departmentalObjective in department_objectives:
            for strategicResult in strategic_results:
                if departmentalObjective == strategicResult.departmental_objective:
                    for performance_measure in performance_measures:
                        if performance_measure.strategic_result == strategicResult:
                            row_num += 1
                            pm = performance_measure
                            row = [request.GET.get('department'), performance_measure.id, pm]
                            for col_num in range(len(row)):
                                ws.write(row_num, col_num, row[col_num])
        wb.save(response)
        
        return response
    
    if request.method == 'POST':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="par_quarters.xls"'
        wb = xlwt.Workbook()
        ws = wb.add_sheet('QuarterlyPar')
        
        # sheet header first row
        row_num = 0
        columns = ['Department', 'ID','Measure', 'Quarter_1(30-06)', 'Quarter_2(30-09)', 'Quarter_3(31-12)', 'Quarter_4(31-03)']
        # columns = ['Department', 'ID','Measure', ]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for departmentalObjective in department_objectives:
            for strategicResult in strategic_results:
                if departmentalObjective == strategicResult.departmental_objective:
                    for performance_measure in performance_measures:
                        if performance_measure.strategic_result == strategicResult:
                            row_num += 1
                            performance_measure_actual_results = ''
                            for formulae in formula:
                                if formulae.performance_measure == performance_measure:
                                    performance_measure_actual_results = formulae.performance_measure_actual_results
                            row = [request.GET.get('department'), performance_measure.id, performance_measure.performance_measure, performance_measure_actual_results]
                            for col_num in range(len(row)):
                                ws.write(row_num, col_num, row[col_num])
        wb.save(response)
        
        return response
        # return download_file_as_excel()
        # return redirect(reverse('departments_par') + '?menu=' + menu + '&department=' + request.GET.get('department') + '&item=' + request.GET.get('item'))    
    
    context = {
        'menu': menu,
        'item': item,
        'initialTemplate': initialTemplate,
        'departments': all_departments,
        'department_template_exists_in_initial_template': department_template_exists_in_initial_template,
        'perspectives': perspectives,
        'perspectives_in_objectives_list': perspectives_in_objectives_list,
        'departmental_objectives': department_objectives,
        'strategic_results': strategic_results,
        'performance_measures': performance_measures,
        'departmental_initiatives': departmental_initiatives,
        'deliverables': deliverables,
        'formulas': formula,
        'actual_expenditures': actual_expenditures,
        'achievements_challenges': achievements_challenges,
    }
    
    return render(request, 'strategy/departments_par.html', context)

# TEMPLATES
def templates_info(request):
    menu = request.GET.get('menu')
    templateForm = InitialTemplateDetailForm()
    logged_in_user = CustomUserRegistration.objects.get(id=request.user.id)
    

    # if request.method == 'POST':
    #     # check for open templates
    #     open_templates = InitialTemplateDetail.objects.all()
        
    #     for temp_open in open_templates:
    #         if temp_open.template_Status == 'open':
    #             temp_open.template_Status = 'close'
    #             temp_open.save()
    #         elif temp_open.template_Status == 'in progress':
    #             temp_open.template_Status = 'queued'
    #             temp_open.save()
        
    #     templateForm = InitialTemplateDetailForm(request.POST)
    #     template_status = request.POST.get('template_status')

    #     if templateForm.is_valid():
    #         templateFormInstance = templateForm.save(commit=False)
    #         templateFormInstance.template_Status = template_status
    #         templateFormInstance.created_by = logged_in_user
    #         templateFormInstance.user_is_strategy = logged_in_user.is_strategy
    #         templateFormInstance.save()
    #         return redirect(reverse('templates') + '?menu=' + menu)
        
    get_templates_info = InitialTemplateDetail.objects.all()

    context = {
        'menu': menu,
        'templateForm': templateForm,
        'templates_info': get_templates_info
    }
    return render(request, 'strategy/templates.html', context)


# Send email view
def send_email(request):
    try:
        if request.method == "POST":
            with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS
            ) as connection:
                subject = request.POST.get("subject")
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST.get("email"), ]
                message = request.POST.get("message")

                # Print the captured data to the terminal
                print("Subject:", subject)
                print("Email:", email_from)
                print("Recipient List:", recipient_list)
                print("Message:", message)

                email = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
                email.send()
                messages.success(request, 'Email sent successfully.')

    except Exception as e:
        print(e)
        messages.error(request, 'Failed to send email.')

    return render(request, 'send_email.html')


#### Password Reset
def change_password(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        if profile_obj:
            context['user_id'] = profile_obj.user.id

            if request.method == 'POST':
                new_password = request.POST.get('password1')
                confirm_password = request.POST.get('password2')
                user_id = request.POST.get('user_id')

                if not user_id:
                    messages.error(request, 'No user id found.')
                elif new_password != confirm_password:
                    messages.error(request, 'Password mismatch, both passwords should match.')
                else:
                    user_obj = CustomUserRegistration.objects.get(id=user_id)
                    user_obj.set_password(new_password)
                    user_obj.save()
                    return redirect('userLogin')
        else:
            messages.error(request, 'No user found for the given token.')

    except Exception as e:
        print(e)

    return render(request, 'reset_password.html', context)



## Forgot Password
import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not CustomUserRegistration.objects.filter(username=username).exists():
                messages.error(request, 'No user found with username')
                return redirect('forgot_password')

            user_obj = CustomUserRegistration.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj, created = Profile.objects.get_or_create(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'Email sent successfully. Please check your Gmail account for the new password link.')
            return redirect('forgot_password')

    except Exception as e:
        print(e)
    return render(request, 'forget_password.html')



##Setting page
def settings_page(request):
    return render(request, 'settings.html')



def adminSettings(request):
    return render(request, 'adminSettings.html')

    


