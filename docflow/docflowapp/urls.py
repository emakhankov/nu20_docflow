from django.urls import path
from docflowapp import views


app_name = 'blogapp'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('search/', views.search_view, name='search'),
]
