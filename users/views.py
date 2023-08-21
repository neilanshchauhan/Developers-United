from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Profile, Message
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles

# Create your views here.
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'user-account')
        else:
            messages.error(request,'Username OR Password is incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.success(request,'User was successfuly logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User was successfully Registered!")

            login(request,user)
            return redirect('edit-account')

        else:
            messages.error(request, "An error occured during Registration!")

    context = {'page':page,'form':form}
    return render(request, 'users/login_register.html',context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)

    context = {'profiles': profiles,'search_query':search_query,'custom_range':custom_range}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    skills = profile.skill_set.all()
    context = {'profile':profile,'skills':skills}
    return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.projects_set.all()
    context = {'profile':profile,'skills':skills,'projects':projects}
    return render(request,'users/account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user-account')
        
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    page = 'create-skill'
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,"Skill has been added!")
            return redirect("user-account")

    context = {'form':form,'page':page}
    return render(request, 'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    page = 'update-skill'
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill has been updated!")
            return redirect("user-account")

    context = {'form':form, 'page':page}
    return render(request, 'users/skill_form.html',context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request,"Skill has been Deleted!")
        return redirect('user-account')
    context = {'object':skill}
    return render(request,'delete_template.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    msg = profile.messages.all()
    unread_msg = msg.filter(is_read=False).count()
    context = {'msg':msg,'unread_msg':unread_msg}
    return render(request,"users/inbox.html",context)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    msg = profile.messages.get(id=pk)
    
    if msg.is_read == False:
        msg.is_read = True
        msg.save()

    context = {'msg':msg}
    return render(request, "users/message.html",context)


def createMessage(request,pk):
    recipient =  Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Message has been sent!")
            return redirect('profile',pk=recipient.id)

    context = {'recipient':recipient,'form':form}
    return render(request, "users/message_form.html",context)