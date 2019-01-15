from django.urls import path, re_path
from haptest import views
from django.contrib.auth.decorators import login_required

app_name = 'haptest'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add_project/', views.add_project, name='add_project'),
    path('add_project/<int:project_id>/', views.add_project, name='add_project'),
    path('project/', views.project_list, name='project'),
    path('project_delete/', views.project_delete, name='project_delete'),
    path('element/', views.element_list, name='element'),
    path('element_delete/', views.element_delete, name='element_delete'),
    path('element_add/<int:id>/', views.element_add, name='element_add'),
    path('element_upload', views.element_upload, name='element_upload'),
    path('testcase', views.testcase_list, name='testcase'),
    path('testcase_add/<int:id>/', views.testcase_add, name='testcase_add'),
    path('testcase_delete/', views.testcase_delete, name='testcase_delete'),
    path('testcase_upload/', views.testcase_upload, name='testcase_upload'),
    path('page_element/<str:page>/', views.get_page_of_elelemt, name='page_element'),
    # path('run_case/', views.run_case, name='run_case_list'),
    path('run_case/', views.run_case, name='run_case'),
    path('run_case_delete/', views.run_case_delete, name='run_case_delete'),
    path('run_case_add/<int:id>/', views.run_case_add, name='run_case_add'),
    path('environment_add/<int:pk>/', views.environment_add, name='environment_add'),
    path('environment/', views.environment, name='environment'),

]
