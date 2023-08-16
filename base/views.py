from django.shortcuts import render,redirect
from .models import Projects
from .forms import ProjectForm

# Create your views here.

def projects(request):
    projects = Projects.objects.all()
    context = {'projects':projects}
    return render(request, 'base/projects.html',context)

def project(request,pk):
    projectObj = Projects.objects.get(id=pk)
    context = {'project':projectObj}
    return render(request,'base/single-project.html',context)

def createProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {'form':form}
    return render(request, 'base/project_form.html',context)

def updateProject(request,pk):
    project = Projects.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST,  request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {'form':form}
    return render(request, 'base/project_form.html',context)

def deleteProject(request,pk):
    project = Projects.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {'object':project}
    return render(request,'base/delete_template.html',context)