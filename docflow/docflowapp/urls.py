from django.urls import path, include
from rest_framework import routers

from docflowapp import views
from docflowapp import viewsets

app_name = 'docflowapp'


router = routers.DefaultRouter()
router.register(r'tasks', viewsets.TaskViewSet)
router.register(r'usertasks', viewsets.UserTaskViewSet, basename='Task')
router.register(r'documents', viewsets.DocumentViewSet)
router.register(r'documenttypes', viewsets.DocumentTypeViewSet)
router.register(r'classifiers', viewsets.ClassifierViewSet)
router.register(r'counterparts', viewsets.CounterpartViewSet)
router.register(r'users', viewsets.UserViewSet)

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('p_documents', views.IndexViewDocuments.as_view(), name='p_index_documents'),
    path('p_tasks', views.IndexViewTasks.as_view(), name='p_index_tasks'),
    path('search', views.SearchView.as_view(), name='search'),
    path('document/<int:pk>', views.DocumentView.as_view(), name='document_view'),
    path('document/add', views.DocumentAdd.as_view(), name='document_add'),
    path('document/<int:pk>/addTask', views.TaskAdd.as_view(), name='task_add'),
    path('task/<int:pk>', views.TaskView.as_view(), name='task_view'),
    path('api/', include(router.urls)),
    path('api/v0/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
