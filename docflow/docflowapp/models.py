from django.db import models
from usersapp.models import DocFlowUser
# Create your models here.




class SysDateAddEdit(models.Model):
    """
    Абстрактный класс для системной информации
    """

    class Meta:
        abstract = True

    sys_date_add = models.DateTimeField(auto_now_add=True)
    sys_date_edit = models.DateTimeField(auto_now=True)
    sys_user_add = models.ForeignKey(DocFlowUser, on_delete=models.DO_NOTHING, null=True)


class Task(SysDateAddEdit):
    """
    Задачи
    """

    name = models.CharField(max_length=255, unique=False)
    description = models.TextField(blank=True)
    date = models.DateField()
    user_to = models.ForeignKey(DocFlowUser, on_delete=models.DO_NOTHING, related_name='user_to')

    def documents_for_template(self):
        return self.document_set.select_related('type', 'sys_user_add').all().prefetch_related('counterpart', 'classifier')

class DocumentType(SysDateAddEdit):
    """
    Классы документов
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Classifier(SysDateAddEdit):
    """
    Классификатор
    Значение классификатора может соответствовать нескольким типам документов
    """
    name = models.CharField(max_length=255, unique=True)
    document_type = models.ManyToManyField(DocumentType)

    def __str__(self):
        return self.name


class Counterpart(SysDateAddEdit):
    """
    Контрагенты
    """
    name = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, unique=True)
    tax_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Document(SysDateAddEdit):
    """
    Карточки документов
    """
    type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    date = models.DateField()
    counterpart = models.ManyToManyField(Counterpart, blank=True, null=True)
    description = models.TextField(blank=True)
    classifier = models.ManyToManyField(Classifier)
    Tasks = models.ManyToManyField(Task, blank=True)

    def counterparts(self):

        return ", ".join([item.name for item in self.counterpart.all()])

    def classifiers(self):

        return ", ".join([item.name for item in self.classifier.all()])

    def tasks_for_template(self):
        return self.Tasks.select_related("sys_user_add", "user_to")

    def __str__(self):
        return f'{self.type} № {self.nom} от {self.date}'



class DocumentConnection(models.Model):
    """
    Связь документов
    """
    parent = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='parent_document')
    child = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='child_document')
    sys_date_add = models.DateTimeField(auto_now_add=True)


class DocumentVersion(SysDateAddEdit):
    """
    Версии документов
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    version_date = models.DateField()








