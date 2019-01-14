from django.forms import inlineformset_factory
from django.urls import reverse
# from django.views import generic
# from .models import Choice, Question,Project
# from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
import os
from haptest.utils.common import dic2database, upload2dicts,testcase2database
from .forms import AddProjectForm, AddElementForm, AddTestCaseForm, AddCaseStepForm, get_CaseStepFormSet, RunCaseForm
from django.contrib import auth
from django.contrib.auth.models import User
from haptest.models import Project, Element, Platform, TestCase, CaseStep, RunCase, Module
from sweetest.runcase import Autotest4database


def register(request):
    # 注册
    if request.method == 'GET':
        return render(request, 'haptest/register.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        User.objects.create_user(username=name, password=password)
        return HttpResponseRedirect('/haptest/login/')


def login(request):
    # 登录
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
            return render(request, 'haptest/login.html', '请输入登录名')


def logout(request):
    # 退出
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect('/haptest/login')


def index(request):
    return render(request, 'haptest/index.html', )


# @login_required
def add_project(request, project_id):
    if request.method == 'POST':
        if project_id != 0:
            form = AddProjectForm(request.POST, instance=Project.objects.get(id=project_id))
        else:
            form = AddProjectForm(request.POST)
        if form.is_valid():
            # Project.objects.create(project_name=form.cleaned_data['project_name'])
            # Project.objects.create(platform=form.cleaned_data['platform'])
            # return render(request,'haptest/add_project.html')
            form.save()
            return HttpResponseRedirect(reverse('haptest:project'))

    else:
        if project_id != 0:
            form = AddProjectForm(instance=Project.objects.get(id=project_id))
        else:
            form = AddProjectForm()
        return render(request, 'haptest/add_project.html', {'form': form, 'project_id': project_id})


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
        choice_set = request.POST.getlist('projects_choice')
    except KeyError:
        return project_list(request)
    else:
        Project.objects.filter(id__in=choice_set).delete()
        # print(request.POST.getlist('projects_choice'),request.POST,choice_set)
        # print(request.POST.itervalues)
        return project_list(request)


# @login_required
def element_add(request, id):
    if request.method == 'POST':
        if id != 0:
            form = AddElementForm(request.POST, instance=Element.objects.get(id=id))
        else:
            form = AddElementForm(request.POST)
        if form.is_valid():
            # Project.objects.create(project_name=form.cleaned_data['project_name'])
            # Project.objects.create(platform=form.cleaned_data['platform'])
            # return render(request,'haptest/add_project.html')
            form.save()
            return HttpResponseRedirect(reverse('haptest:element'))

    else:
        if id != 0:
            form = AddElementForm(instance=Element.objects.get(id=id))
        else:
            form = AddElementForm()
        return render(request, 'haptest/element_add.html', {'form': form, 'element_id': id})


# @login_required
def element_list(request):
    manage_info = {
        'data_set': Element.objects.all(),
        'platform': Platform.objects.all(),
    }
    return render(request, 'haptest/element_list.html', manage_info)


# @login_required
def element_delete(request):
    try:
        choice_set = request.POST.getlist('elements_choice')
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
    # 元素上传
    if request.method == 'POST':
        try:
            platform_id = request.POST.get('platform')
        except KeyError as e:
            return JsonResponse({"status": '【所属平台】不能为空'})
        if platform_id is None:
            return JsonResponse({"status": '【所属平台】不能为空'})
        file_obj = request.FILES.get('upload')
        ele_dics=upload2dicts(file_obj,platform=platform_id)
        dic2database(ele_dics,Element)
        # upload_file = os.path.join('upload', file_obj.name)
        # with open(upload_file, 'wb') as data:
        #     for line in file_obj.chunks():
        #         data.write(line)
        # file2database(upload_file, Element, platform_id)
        return JsonResponse({'status': reverse('haptest:element')})

# @login_required
def testcase_list(request):
    manage_info = {
        'data_set': TestCase.objects.all(),
        'platform': Platform.objects.all(),
        'module': Module.objects.all(),

    }
    return render(request, 'haptest/testcase_list.html', manage_info)

# @login_required
def testcase_add(request, id):
    if request.method == 'POST':
        if id != 0:
            form = AddTestCaseForm(request.POST, instance=TestCase.objects.get(id=id))
        else:
            form = AddTestCaseForm(request.POST)
        if form.is_valid():
            testcase = form.save()
            casestep_formset = get_CaseStepFormSet()(request.POST, instance=testcase)
            if casestep_formset.is_valid():
                casestep_formset.save()
                return HttpResponseRedirect(reverse('haptest:testcase'))
            else:
                # return HttpResponse("用例步骤保存失败" + str(casestep_formset.errors))
                return render(request, 'haptest/testcase_add.html', {'form': form,
                                                                     'testcase_id': id,
                                                                     'casestep_form_set': casestep_formset,
                                                                     })
        else:
            return render(request, 'haptest/testcase_add.html', {'form': form,
                                                                 'testcase_id': id,
                                                                 # 'casestep_form_set': casestep_formset,
                                                                 })

    else:
        if id != 0:
            testcase_data = TestCase.objects.get(id=id)
            form = AddTestCaseForm(instance=testcase_data)
            casestep_formset = get_CaseStepFormSet()(instance=testcase_data)
        else:
            form = AddTestCaseForm()
            casestep_formset = get_CaseStepFormSet(extra=1)()
        return render(request, 'haptest/testcase_add.html', {'form': form,
                                                             'testcase_id': id,
                                                             'casestep_form_set': casestep_formset,
                                                             })

# @login_required
def testcase_delete(request):
    try:
        choice_set = request.POST.getlist('data_choice')
    except KeyError:
        return project_list(request)
    else:
        TestCase.objects.filter(id__in=choice_set).delete()
        return testcase_list(request)

@csrf_exempt
# @login_required
def testcase_upload(request):
    # 元素上传
    if request.method == 'POST':
        try:
            platform_id ,module_id= request.POST.get('platform'),request.POST.get("module")
        except KeyError as e:
            return JsonResponse({"status": '【所属平台】、或所属模块不能为空'})
        if platform_id is None:
            return JsonResponse({"status": '【所属平台】不能为空'})
        file_obj = request.FILES.get('upload')
        case_dicts=upload2dicts(file_obj,platform_id=platform_id,module_name_id=module_id)
        testcase2database(case_dicts)
        return JsonResponse({'status': reverse('haptest:testcase')})

def get_page_of_elelemt(request, page):
    # 获取页面元素
    if request.method == 'GET':
        e_obj = Element.objects.all()
        ele = []
        page_ele_dic = {}
        for e in e_obj:
            if page_ele_dic.get(e.page, None):
                page_ele_dic[e.page].append(e.element)
            else:
                page_ele_dic[e.page] = [e.element]
        elements = page_ele_dic[page]
    return render(request, 'haptest/page_element.html', {'elements': elements})

# @login_required
def run_case_add(request, id):
    if request.method == 'POST':
        if id != 0:
            form = RunCaseForm(request.POST, instance=RunCase.objects.get(id=id))
        else:
            form = RunCaseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('haptest:run_case'))

    else:
        if id != 0:
            form = RunCaseForm(instance=RunCase.objects.get(id=id))
        else:
            form = RunCaseForm()
        return render(request, 'haptest/run_case_add.html', {'form': form, 'run_case_id': id})

# @login_required
def run_case(request, id=None):
    # 执行用例
    if request.method == "POST":
        choice_id = request.POST.get('run_case_choice_submit')
        runobj = RunCase.objects.get(pk=int(choice_id))
        run_obj=Autotest4database(run_case_obj=RunCase.objects.get(pk=int(choice_id)))
        run_obj.plan()
        return HttpResponse("执行用例成功")
    else:
        manage_info = {
            'data_set': RunCase.objects.all(),
            # 'module': Project.objects.all(),
        }
        return render(request, 'haptest/run_case_list.html', manage_info)

# @login_required
def run_case_delete(request):
    if request.method == "POST":
        choice_set = request.POST.getlist('run_case_choice')
        if choice_set:
            RunCase.objects.filter(id__in=choice_set).delete()
            return HttpResponse("删除数据成功")
        else:
            return HttpResponse("没有选择数据")
