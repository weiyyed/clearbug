from django.urls import reverse
# from django.views import generic
# from .models import Choice, Question,Project
# from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .forms import AddProjectForm
from django.contrib import auth
from django.contrib.auth.models import User
from haptest.models import Project


def register(request):
    #注册
    if request.method == 'GET':
        return render(request, 'haptest/register.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        User.objects.create_user(username=name, password=password)
        return HttpResponseRedirect('/haptest/login/')


def login(request):
    #登录
    if request.method == 'GET':
        return render(request, 'haptest/login.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 验证用户名和密码，通过的话，返回User对象
        user = auth.authenticate(username=name, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect('/haptest/')
        else:
            return render(request, 'haptest/login.html','请输入登录名')
def logout(request):
    # 退出
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect('/haptest/login')

def index(request):
    return render(request, 'haptest/index.html', )

# @login_required
def add_project(request,project_id):

    if request.method=='POST':
        if project_id !=0:
            form=AddProjectForm(request.POST,instance=Project.objects.get(id=project_id))
        else:
            form=AddProjectForm(request.POST)
        if form.is_valid():
            # Project.objects.create(project_name=form.cleaned_data['project_name'])
            # Project.objects.create(platform=form.cleaned_data['platform'])
            # return render(request,'haptest/add_project.html')
            form.save()
            return HttpResponseRedirect(reverse('haptest:project'))

    else:
        if project_id !=0:
            form=AddProjectForm(instance=Project.objects.get(id=project_id))
        else:
            form=AddProjectForm()
        return render(request,'haptest/add_project.html',{'form':form,'project_id':project_id})


def project_list(request):
    # return render(request, 'haptest/project_list.html', )
    # filter_query = set_filter_session(request)
    # pro_list = get_pager_info(
    #     Project, filter_query, '/api/project_list/', id)
    manage_info = {
        # 'account': account,
        'projects': Project.objects.all(),
        # 'page_list': pro_list[0],
        # 'info': filter_query,
        # 'sum': pro_list[2],
        # 'env': EnvInfo.objects.all().order_by('-create_time'),
        # 'project_all': Project.objects.all(),
    }
    return render(request, 'haptest/project_list.html', manage_info)