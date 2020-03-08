from django.db import models

# Create your models here.


class Task(models.Model):
    """
    Задачи
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    sys_date_add = models.DateTimeField(auto_now_add=True)
    sys_date_edit = models.DateTimeField(auto_now=True)


class DocumentType(models.Model):
    """
    Классы документов
    """
    name = models.CharField(max_length=255, unique = True)
    sys_date_add = models.DateTimeField(auto_now_add=True)
    sys_date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Classifier(models.Model):
    """
    Классификатор
    Значение классификатора может соответствовать нескольким типам документов
    """
    name = models.CharField(max_length=255, unique = True)
    document_type = models.ManyToManyField(DocumentType)
    sys_date_add = models.DateTimeField(auto_now_add=True)
    sys_date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Counterpart(models.Model):
    """
    Контрагенты
    """
    name = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, unique=True)
    tax_number = models.CharField(max_length=50, unique=True)
    sys_date_add = models.DateTimeField(auto_now_add=True)
    sys_date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    """
    Карточки документов
    """
    type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    date = models.DateField()
    counterpart = models.ManyToManyField(Counterpart, blank=True)
    description = models.TextField(blank=True)
    classifier = models.ManyToManyField(Classifier)
    sys_date_add = models.DateTimeField(auto_now_add=True)
    sys_date_edit = models.DateTimeField(auto_now=True)
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


class DocumentVersion(models.Model):
    """
    Версии документов
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    version_date = models.DateField()
    sys_date_add = models.DateTimeField(auto_now_add=True)
    sys_date_edit = models.DateTimeField(auto_now=True)







