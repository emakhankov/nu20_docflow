from django.contrib import admin

from .models import Task
from .models import DocumentType, Classifier, Counterpart, Document, DocumentConnection, DocumentVersion
# Register your models here.

admin.site.register(Task)

admin.site.register(DocumentType)
admin.site.register(Classifier)
admin.site.register(Counterpart)
admin.site.register(Document)
admin.site.register(DocumentConnection)
admin.site.register(DocumentVersion)
