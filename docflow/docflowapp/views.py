from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from .models import Task, Document
from .forms import SearchForm, DocumentAddEditForm, TaskAddEditForm
from django.views.generic import View, TemplateView, FormView, CreateView, DetailView
from django.views.generic.base import ContextMixin

from django.db.models import Q
# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Здесь стартовая страница, поэтому не будем отображать ее как
    """

    template_name = 'docflowapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.all().order_by('-date')[:5]
        tasks = Task.objects.filter(user_to=self.request.user).order_by('-date')[:5]
        context['nbar'] = 'index'
        context['documents'] = documents
        context['tasks'] = tasks
        return context


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
            documents = q1.all()
            documents_count = documents.count()
            return render(request, 'docflowapp/searchResult.html', context={'nbar': 'search', 'documents': documents, 'documents_count': documents_count})

        else:
            return render(request, 'docflowapp/search.html', context={'nbar': 'search', 'search_form': search_form})


class DocumentView(LoginRequiredMixin, DetailView):

    model = Document
    template_name = 'docflowapp/documentView.html'
    context_object_name = 'document'


class DocumentAdd(LoginRequiredMixin, UserPassesTestMixin, CreateView):


    #fields = '__all__'
    #model = Document
    #fields = ('type', 'nom', 'date', 'counterpart', 'description', 'classifier')

    form_class = DocumentAddEditForm
    # Мы пойдем на URL с параметром
    #success_url = reverse_lazy('docflowapp:index')
    template_name = 'docflowapp/documentAdd.html'

    def test_func(self):
        return self.request.user.can_add_documents

    #def handle_no_permission(self):
     #   return redirect('users:create-profile')

    def form_valid(self, form):

        # self.request.user - текущий пользователь
        form.instance.sys_user_add = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        print('Добавилось', self.object.id)
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

#def index_view(request):
#
#    documents = Document.objects.all().order_by('-date')[:5]
#    tasks = Task.objects.all().order_by('-date')[:5]
#    return render(request, 'docflowapp/index.html', context={'nbar': 'index', 'documents': documents, 'tasks': tasks})


#def search_view(request):
#
#    if request.method == 'POST':
#        return render(request, 'docflowapp/UnderConstruction.html')
#    else:
#
#        return render(request, 'docflowapp/search.html', context={'nbar': 'search', 'search_form': search_form })


