from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question,Project
from .forms import AddProject
from .forms import AddForm

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
def add_project(request):
    if request.method=='POST':
        form=AddProject(request.POST)
        if form.is_valid():
            Project.objects.create(project_name=form.cleaned_data['project_name'])

            # return render(request,'haptest/add_project.html')
            return render(request, 'haptest/add_project.html', {'form': form})

    else:
        form=AddProject()
    # return render(request, 'haptest/index.html', {'form': form})
    return render(request,'haptest/add_project.html',{'form':form})

#
# def index(request):
#     return render(request, 'index.html')


def index(request):
    if request.method == 'POST':  # 当提交表单时

        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))

    else:  # 当正常访问时
        form = AddForm()
    return render(request, 'haptest/index.html', {'form': form})