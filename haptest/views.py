from django.urls import reverse
# from django.views import generic
# from .models import Choice, Question,Project
# from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

import os

from haptest.utils.common import file2database
from .forms import AddProjectForm, AddElementForm, AddTestCaseForm
from django.contrib import auth
from django.contrib.auth.models import User
from haptest.models import Project, Element, Plateform, TestCase


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

# @login_required
def project_list(request):
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

# @login_required
def project_delete(request):

    try:
        choice_set=request.POST.getlist('projects_choice')
    except KeyError:
        return project_list(request)
    else:
        Project.objects.filter(id__in=choice_set).delete()
        # print(request.POST.getlist('projects_choice'),request.POST,choice_set)
        # print(request.POST.itervalues)
        return project_list(request)

# @login_required
def element_add(request,id):

    if request.method=='POST':
        if id !=0:
            form=AddElementForm(request.POST,instance=Element.objects.get(id=id))
        else:
            form=AddElementForm(request.POST)
        if form.is_valid():
            # Project.objects.create(project_name=form.cleaned_data['project_name'])
            # Project.objects.create(platform=form.cleaned_data['platform'])
            # return render(request,'haptest/add_project.html')
            form.save()
            return HttpResponseRedirect(reverse('haptest:element'))

    else:
        if id !=0:
            form=AddElementForm(instance=Element.objects.get(id=id))
        else:
            form=AddElementForm()
        return render(request,'haptest/element_add.html',{'form':form,'element_id':id})


# @login_required
def element_list(request):
    manage_info = {
        'data_set': Element.objects.all(),
        'platform':Plateform.objects.all(),
    }
    return render(request, 'haptest/element_list.html', manage_info)

# @login_required
def element_delete(request):

    try:
        choice_set=request.POST.getlist('elements_choice')
    except KeyError:
        return project_list(request)
    else:
        Element.objects.filter(id__in=choice_set).delete()
        # print(request.POST.getlist('projects_choice'),request.POST,choice_set)
        # print(request.POST.itervalues)
        return element_list(request)

@csrf_exempt
# @login_required
def element_upload(request):
    #元素上传
    if request.method=='POST':
        try:
            platform_id=request.POST.get('platform')
        except KeyError as e:
            return JsonResponse({"status":'【所属平台】不能为空'})
        if platform_id is None:
            return JsonResponse({"status": '【所属平台】不能为空'})
        file_obj=request.FILES.get('upload')
        upload_file=os.path.join('upload',file_obj.name)
        with open(upload_file,'wb') as data:
            for line in file_obj.chunks():
                data.write(line)
        file2database(upload_file,Element,platform_id)
        return JsonResponse({'status': reverse('haptest:element')})

# @login_required
def testcase_list(request):
    manage_info = {
        'data_set': TestCase.objects.all(),
        'platform':Plateform.objects.all(),
    }
    return render(request, 'haptest/testcase_list.html', manage_info)

# @login_required
def testcase_add(request,id):

    if request.method=='POST':
        if id !=0:
            form=AddTestCaseForm(request.POST,instance=TestCase.objects.get(id=id))
        else:
            form=AddTestCaseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('haptest:testcase'))

    else:
        if id !=0:
            form=AddTestCaseForm(instance=TestCase.objects.get(id=id))
        else:
            form=AddTestCaseForm()
        return render(request, 'haptest/testcase_add.html', {'form': form, 'testcase_id': id})
# @login_required
def testcase_delete(request):

    try:
        choice_set=request.POST.getlist('data_choice')
    except KeyError:
        return project_list(request)
    else:
        TestCase.objects.filter(id__in=choice_set).delete()
        return testcase_list(request)