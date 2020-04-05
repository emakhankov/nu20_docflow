from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class DocFlowUser(AbstractUser):

    can_add_documents = models.BooleanField(verbose_name='can create documents', default=False)
    can_find_documents = models.BooleanField(verbose_name='can find documents', default=False)
