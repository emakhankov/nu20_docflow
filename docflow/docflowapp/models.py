from django.db import models

# Create your models here.


class SysDateAddEdit(models.Model):
    """
    Абстрактный класс для системной информации
    """

    class Meta:
        abstract = True

    sys_date_add = models.DateTimeField(auto_now_add=True)
    sys_date_edit = models.DateTimeField(auto_now=True)


class Task(SysDateAddEdit):
    """
    Задачи
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    date = models.DateField()


class DocumentType(SysDateAddEdit):
    """
    Классы документов
    """
    name = models.CharField(max_length=255, unique= True)

    def __str__(self):
        return self.name


class Classifier(SysDateAddEdit):
    """
    Классификатор
    Значение классификатора может соответствовать нескольким типам документов
    """
    name = models.CharField(max_length=255, unique = True)
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
    counterpart = models.ManyToManyField(Counterpart, blank=True)
    description = models.TextField(blank=True)
    classifier = models.ManyToManyField(Classifier)
    Tasks = models.ManyToManyField(Task, blank=True)

    def counterparts(self):

        return ", ".join([item.name for item in self.counterpart.all()])

    def classifiers(self):

        return ", ".join([item.name for item in self.classifier.all()])

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








