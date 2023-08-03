from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


# Create your views here.
@login_required
def manager(request):
    projects = Project.objects.filter(user=request.user)
    project_form = ProjectForm()
    processes = Process.objects.filter(user=request.user)
    process_form = ProcessForm()
    activities = Activity.objects.filter(user=request.user)
    activity_form = ActivityForm()

    if request.method == 'POST':
        # if "create_project_form" in request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid:
            project = form.save(commit=False)
            project.user = request.user 
            project.save() 


    context = {
        'projects' : projects,
        'project_form' : project_form,
        'processes' : processes,
        'process_form' : process_form,
        'activities' : activities,
        'activity_form' : activity_form,

    }

    return render(request, 'project_manager/manager.html', context)

@login_required
def project(request, primary_key_project):
    project = Project.objects.get(id=primary_key_project)

    if(project.user != request.user):
        return redirect('manager')

    processes = Process.objects.filter(project=project)
    activities = Activity.objects.filter(project=project)
    project_form = ProjectForm(instance=project)
    process_form = ProcessForm()
    activity_form = ActivityForm()

    

    if request.method == 'POST':    
        if "create_process_btn" in request.POST:
            form = ProcessForm(request.POST)
            if form.is_valid:
                process = form.save(commit=False)
                process.project = project
                process.user = request.user
                process.save()
        elif "edit_project_form" in request.POST:
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid:
                form.save()


    context = {
        'project' : project,
        'processes' : processes,
        'activities' : activities,
        'process_form' : process_form,
        'activity_form' : activity_form,
        'primary_key_project' : primary_key_project,
        'project_form' : project_form,

    }

    return render(request, 'project_manager/project.html', context)

@login_required
def process(request, primary_key_project, primary_key_process):
    project = Project.objects.get(id=primary_key_project)
    process = Process.objects.get(id=primary_key_process)
    activities = Activity.objects.filter(process=process)
    process_form = ProcessForm(instance=process)
    activity_form = ActivityForm()

    if(project.user != request.user):
        return redirect('manager')

    if request.method == 'POST':
        if "create_activity_form" in request.POST:
            form = ActivityForm(request.POST)
            if form.is_valid:
                activity = form.save(commit=False)
                activity.project = project
                activity.process = process
                activity.user = request.user
                activity.save()
        elif "edit_process_form" in request.POST:
            form = ProcessForm(request.POST, instance=process)
            if form.is_valid:
                form.save()


    context = {
        'project' : project,
        'process' : process,
        'activities' : activities,
        'process_form' : process_form,
        'activity_form' : activity_form,

    }

    return render(request, 'project_manager/process.html', context)

@login_required
def edit_activity(request, primary_key_project, primary_key_process, primary_key_activity):
    project = Project.objects.get(id=primary_key_project)
    process = Process.objects.get(id=primary_key_process)
    activity = Activity.objects.get(id=primary_key_activity)
    activity_form = ActivityForm(instance=activity)

    if(project.user != request.user):
        return redirect('manager')

    if request.method == 'POST':
        # if "create_project_form" in request.POST:
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid:
            form.save()
            return redirect('process', primary_key_project, primary_key_process)


    context = {
        'project' : project,
        'process' : process,
        'activity' : activity,
        'activity_form' : activity_form,

    }

    return render(request, 'project_manager/edit_activity.html', context)

@login_required
def delete_project(request, primary_key_project):
    project = Project.objects.get(id=primary_key_project)
    project.delete()

    return redirect('manager')
@login_required
def delete_process(request, primary_key_project, primary_key_process):
    process = Process.objects.get(id=primary_key_process)
    process.delete()

    return redirect('project', primary_key_project)
@login_required
def delete_activity(request, primary_key_project, primary_key_process, primary_key_activity):
    activity = Activity.objects.get(id=primary_key_activity)
    activity.delete()

    return redirect('process', primary_key_project, primary_key_process)