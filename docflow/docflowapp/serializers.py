from rest_framework import serializers

from .models import Task, Document, DocumentType, Classifier, Counterpart
from usersapp.models import DocFlowUser


class DocumentTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DocumentType
        fields = ['id', 'name']


class CounterpartSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Counterpart
            fields = ['id', 'name', 'full_name', 'tax_number']


class ClassifierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classifier
        fields = ['id', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DocFlowUser
        fields = ['id', 'username', 'can_find_documents', 'can_add_documents']


class UserShortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DocFlowUser
        fields = ['id', 'username']


class DocumentShortSerializer(serializers.HyperlinkedModelSerializer):
    type = DocumentTypeSerializer(many=False, read_only=True)
    counterpart = CounterpartSerializer(many=True, read_only=True)
    classifier = ClassifierSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'type', 'nom', 'date', 'counterpart', 'description', 'classifier']


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    user_to = UserShortSerializer(many=False, read_only=True)
    sys_user_add = UserShortSerializer(many=False, read_only=True)
    Documents = DocumentShortSerializer(many=True, read_only=True, source='document_set')

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'date', 'user_to', 'sys_date_add', 'sys_user_add', 'Documents']


class TaskShortSerializer(serializers.HyperlinkedModelSerializer):

    user_to = UserShortSerializer(many=False, read_only=True)
    sys_user_add = UserShortSerializer(many=False, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'date', 'user_to', 'sys_date_add', 'sys_user_add']





class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    type = DocumentTypeSerializer(many=False, read_only=True)
    counterpart = CounterpartSerializer(many=True, read_only=True)
    classifier = ClassifierSerializer(many=True, read_only=True)
    Tasks = TaskShortSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'type', 'nom', 'date', 'counterpart', 'description', 'classifier', 'Tasks']















