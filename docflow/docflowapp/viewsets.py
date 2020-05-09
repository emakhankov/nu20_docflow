from rest_framework import viewsets

from .models import Task, Document, DocumentType, Classifier, Counterpart
from usersapp.models import DocFlowUser
from .serializers import TaskSerializer, DocumentSerializer, DocumentTypeSerializer, ClassifierSerializer, \
    CounterpartSerializer, UserSerializer


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserTaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user_to=self.request.user).order_by('-date')


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.select_related('type', 'sys_user_add').all().prefetch_related('counterpart', 'classifier', 'Tasks')
    serializer_class = DocumentSerializer


class DocumentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


class ClassifierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Classifier.objects.all()
    serializer_class = ClassifierSerializer


class CounterpartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Counterpart.objects.all()
    serializer_class = CounterpartSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DocFlowUser.objects.all()
    serializer_class = UserSerializer