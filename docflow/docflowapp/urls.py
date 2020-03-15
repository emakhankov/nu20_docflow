from django.urls import path
from docflowapp import views


app_name = 'docflowapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search', views.SearchView.as_view(), name='search'),
    path('document/<int:pk>', views.DocumentView.as_view(), name='document_view'),
    path('document/add', views.DocumentAdd.as_view(), name='document_add'),
    path('document/<int:pk>/addTask', views.TaskAdd.as_view(), name='task_add'),
]
