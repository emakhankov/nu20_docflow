from django.shortcuts import render
from .models import Task, Document
from .forms import SearchForm
# Create your views here.

def index_view(request):
    #posts = Post.objects.all()
    documents = Document.objects.all().order_by('-date')[:5]
    tasks = Task.objects.all().order_by('-date')[:5]
    return render(request, 'docflowapp/index.html', context={'nbar': 'index', 'documents': documents, 'tasks': tasks})


def search_view(request):

    if request.method == 'POST':
        return render(request, 'docflowapp/UnderConstruction.html')
    else:
        search_form = SearchForm()
        return render(request, 'docflowapp/search.html', context={'nbar': 'search', 'search_form': search_form })
