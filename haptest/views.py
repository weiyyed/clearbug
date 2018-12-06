from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from django.views import generic
# from .models import Choice, Question,Project
from .forms import AddProjectForm
from django.contrib import auth
# from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('haptest/index-.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'haptest/index-.html', context)
# def detail(request, question_id):
#     # return HttpResponse("You're looking at question %s." % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'haptest/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'haptest/results.html', {'question': question})

#
# class IndexView(generic.ListView):
#     template_name = 'haptest/index-.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'haptest/detail.html'
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'haptest/results.html'
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'haptest/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('haptest:results', args=(question.id,)))
#
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
# @login_required
def add_project(request):
    if request.method=='POST':
        form=AddProjectForm(request.POST)
        if form.is_valid():
            # Project.objects.create(project_name=form.cleaned_data['project_name'])
            # Project.objects.create(platform=form.cleaned_data['platform'])
            # return render(request,'haptest/add_project.html')
            form.save()
            return render(request, 'haptest/project_list.html')

    else:
        form=AddProjectForm()
    return render(request,'haptest/add_project.html',{'form':form})

#
# def index(request):
#     return render(request, 'index.html')


def index(request):
    return render(request, 'haptest/index.html', )
def project_list(request):
    return render(request, 'haptest/project_list.html', )