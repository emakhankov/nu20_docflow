from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class DocFlowUserCreationForm(UserCreationForm):

    #first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #email = forms.EmailField(max_length=254, required=False)
    #username = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'can_add_documents', 'can_find_documents')