from django.shortcuts import render,redirect
from .models import Projects
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, ReviewForm
from django.db.models import Q
from .models import Projects,Tag
from .utils import searchProjects, paginateProjects
from django.contrib import messages

# Create your views here.

def projects(request):
    projects,search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 3)

    context = {'projects':projects,'search_query':search_query,'custom_range':custom_range}
    return render(request, 'base/projects.html',context)

def project(request,pk):
    projectObj = Projects.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.owner = request.user.profile
        review.project = projectObj
        review.save()
        messages.success(request, "Review has been submitted")
        # Updating Project Vote Count

    context = {'project':projectObj,'form':form}
    return render(request,'base/single-project.html',context)

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("user-account")

    context = {'form':form}
    return render(request, 'base/project_form.html',context)

@login_required(login_url='login')
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST,  request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("user-account")

    context = {'form':form}
    return render(request, 'base/project_form.html',context)

@login_required(login_url='login')
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {'object':project}
    return render(request,'delete_template.html',context)


