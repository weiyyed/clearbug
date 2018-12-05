from django.urls import path,re_path
from haptest import views
# from clearbug.activator import process
from django.contrib.auth.decorators import login_required

app_name = 'haptest'
urlpatterns = [
    # path('', views.index, name='index'),
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),

    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('add_project/',views.add_project,name='add_project'),
    path('', views.index,name='index'),
    # path('', views.index, name='home'),

    # url(r'^admin/', admin.site.urls),
    # re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/assets/img/favicon.ico')),
    # re_path('^(?P<app>(\w+))/(?P<function>(\w+))/$', process),
    # re_path('^(?P<app>(\w+))/(?P<function>(\w+))/(?P<id>(\w+))/$', process),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
]