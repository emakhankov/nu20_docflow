from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from .models import Task, Document
from .forms import SearchForm, DocumentAddEditForm, TaskAddEditForm
from django.views.generic import View, TemplateView, FormView, CreateView, DetailView, ListView
from django.views.generic.base import ContextMixin

from django.db.models import Q


# Вспомогательные пиджинаторы
class FakePaginatorSub1:

    def __init__(self, num_pages):
        self.num_pages = num_pages


class FakePaginator:

    def __init__(self, num_pages):
        self.number = 1
        self.paginator = FakePaginatorSub1(num_pages)


# Вьюхи
class IndexView(LoginRequiredMixin, TemplateView):
    """
    Здесь стартовая страница, поэтому не будем отображать ее как
    """

    template_name = 'docflowapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.select_related('type', 'sys_user_add').all().prefetch_related('counterpart', 'classifier').order_by('-date')[:5]
        documents_page_obj = FakePaginator((Document.objects.count() - 1) // 5 + 1)
        #print(documents_page_obj.number, documents_page_obj.paginator.num_pages)
        #tasks = Task.objects.objects_user_to.order_by('-date')[:5]
        tasks = Task.objects.filter(user_to=self.request.user).select_related('sys_user_add', 'user_to').order_by('-date')[:5]
        tasks_page_obj = FakePaginator((Task.objects.filter(user_to=self.request.user).count() - 1) // 5 + 1)
        context['nbar'] = 'index'
        context['documents'] = documents
        context['documents_page_obj'] = documents_page_obj
        context['tasks'] = tasks
        context['tasks_page_obj'] = tasks_page_obj

        return context


class IndexViewDocuments(ListView):
    """
    Часть стартовой страницы
    """
    paginate_by = 5
    template_name = 'docflowapp/partial_document_list.html'
    context_object_name = 'documents'

    def get_queryset(self):
        return Document.objects.select_related('type', 'sys_user_add').all()\
            .prefetch_related('counterpart', 'classifier').order_by('-date')


class IndexViewTasks(ListView):
    """
    Часть стартовой страницы
    """
    paginate_by = 5
    template_name = 'docflowapp/partial_task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user_to=self.request.user).select_related('sys_user_add', 'user_to').order_by('-date')


class SearchView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Здесь будут по разному отрабатываться get и post запрос
    """

    def test_func(self):
        return self.request.user.can_find_documents

    def get(self, request, *args, **kwargs):
        search_form = SearchForm()
        return render(request, 'docflowapp/search.html', context={'nbar': 'search', 'search_form': search_form})

    def post(self, request, *args, **kwargs):

        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            type = search_form.cleaned_data['type']
            nom = search_form.cleaned_data['nom']
            date_from = search_form.cleaned_data['date_from']
            date_to = search_form.cleaned_data['date_to']
            description = search_form.cleaned_data['description']
            all = search_form.cleaned_data['all']

            q1 = Document.objects
            if type is not None:
                q1 = q1.filter(type=type)
            if nom is not None:
                q1 = q1.filter(nom__istartswith=nom)
            if date_from is not None:
                q1 = q1.filter(date__gte=date_from)
            if date_to is not None:
                q1 = q1.filter(date__lte=date_from)
            if description is not None:
                q1 = q1.filter(description__icontains=description)
            if all is not None:
                q1 = q1.filter(Q(nom__icontains=all) | Q(description__icontains=all))
            documents = q1.select_related('type', 'sys_user_add').all().prefetch_related('counterpart', 'classifier')
            documents_count = documents.count()
            return render(request, 'docflowapp/searchResult.html',
                          context={'nbar': 'search', 'documents': documents, 'documents_count': documents_count})

        else:
            return render(request, 'docflowapp/search.html', context={'nbar': 'search', 'search_form': search_form})


class DocumentView(LoginRequiredMixin, DetailView):
    #model = Document
    queryset = Document.objects.select_related('type', 'sys_user_add')
    template_name = 'docflowapp/documentView.html'
    context_object_name = 'document'


class DocumentAdd(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # fields = '__all__'
    # model = Document
    # fields = ('type', 'nom', 'date', 'counterpart', 'description', 'classifier')

    form_class = DocumentAddEditForm
    # Мы пойдем на URL с параметром
    # success_url = reverse_lazy('docflowapp:index')
    template_name = 'docflowapp/documentAdd.html'

    def test_func(self):
        return self.request.user.can_add_documents

    # def handle_no_permission(self):
    #   return redirect('users:create-profile')

    def form_valid(self, form):
        # self.request.user - текущий пользователь
        form.instance.sys_user_add = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # print('Добавилось', self.object.id)
        return reverse('docflowapp:document_view', args=(self.object.id,))


class TaskAdd(LoginRequiredMixin, CreateView):
    form_class = TaskAddEditForm
    success_url = reverse_lazy('docflowapp:index')
    template_name = 'docflowapp/taskAdd.html'

    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(Document, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # self.request.user - текущий пользователь
        form.instance.sys_user_add = self.request.user
        form.save()
        form.instance.document_set.add(self.document)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # print('Добавилось', self.object.id)
        return reverse('docflowapp:document_view', args=(self.document.pk,))
# def index_view(request):
#
#    documents = Document.objects.all().order_by('-date')[:5]
#    tasks = Task.objects.all().order_by('-date')[:5]
#    return render(request, 'docflowapp/index.html', context={'nbar': 'index', 'documents': documents, 'tasks': tasks})


# def search_view(request):
#
#    if request.method == 'POST':
#        return render(request, 'docflowapp/UnderConstruction.html')
#    else:
#
#        return render(request, 'docflowapp/search.html', context={'nbar': 'search', 'search_form': search_form })


class TaskView(LoginRequiredMixin, DetailView):
    #model = Document
    queryset = Task.objects.select_related('sys_user_add', 'user_to')
    template_name = 'docflowapp/taskView.html'
    context_object_name = 'task'
