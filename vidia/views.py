from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Profile, Project, Tag
from .forms import ProjectForm, TagForm


# index page
def index(request):
    return render(request, 'index.html')

# project


@login_required(login_url='/accounts/login')
def submit_project(request):
    user = request.user

    new_project_form = ProjectForm(request.POST, request.FILES)
    new_tag_form = TagForm(request.POST)
    if user.is_authenticated and new_project_form.is_valid():
        project = new_project_form.save(commit=False)
        project.user_id = user.id
        project.save()
        new_project_form.save_m2m()
        return redirect(index)
    else:
        new_project_form = ProjectForm(request.POST)
        new_tag_form = TagForm(request.POST)

    return render(request, 'new_project.html', {"new_project_form": new_project_form, "new_tag_form": new_tag_form})


@login_required(login_url="/accounts/login")
def create_project_tag(request):
    user = request.user
    new_tag_form = TagForm(request.POST)

    if user.is_authenticated and new_tag_form.is_valid():
        tag = new_tag_form.save(commit=False)
        tag.user = user
        tag.save()
        return redirect(submit_project)
    else:
        new_tag_form = TagForm(request.POST)
    return render(request, 'new_tag.html', {"new_tag_form": new_tag_form})


@login_required(login_url="/accounts/login")
def create_tag(request):
    user = request.user
    new_tag_form = TagForm(request.POST)

    if user.is_authenticated and new_tag_form.is_valid():
        tag = new_tag_form.save(commit=False)
        tag.user = user
        tag.save()
        return redirect(index)
    else:
        new_tag_form = TagForm(request.POST)
    return render(request, 'new_tag.html', {"new_tag_form": new_tag_form})
