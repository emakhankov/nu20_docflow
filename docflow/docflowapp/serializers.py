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
    #type = DocumentTypeSerializer(many=False, read_only=True)
    type_name = serializers.CharField(source='type.name')

    class Meta:
        model = Document
        fields = ['id', 'type_name', 'nom', 'date', 'description', 'classifiers', 'counterparts']

class DocumentIdSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='pk')  # без этой хуйни убил час потому как приезжал пустой document_set

    class Meta:
        model = Document
        fields = ['id']

#class Document1Serializer(serializers.Field):
#
#    def to_representation(self, obj):
#        return obj.document_set[0].id
#
#    def to_internal_value(self, data):
#
#        document = Document.objects.get(data)
#        return document


class TaskSerializer(serializers.ModelSerializer):

    user_to_username = serializers.CharField(source='user_to.username', read_only=False)
    user_to = UserShortSerializer(many=False, read_only=True)
    sys_user_add = UserShortSerializer(many=False, read_only=True)
    Documents = DocumentShortSerializer(many=True, read_only=True, source='document_set')
    #document_id = Document1Serializer(read_only=True)
    document_id = DocumentIdSerializer(many=True, source='document_set')

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'date', 'user_to', 'user_to_username', 'sys_date_add', 'sys_user_add',
                  'Documents', 'document_id']

    def create(self, validated_data):
        print(validated_data)
        print('---------------')

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user


        documents_id_data = validated_data.pop('document_set')
        validated_data['user_to'] = DocFlowUser.objects.get(username=validated_data['user_to']['username'])
        validated_data['sys_user_add'] = user
        print('before create')
        task = Task.objects.create(**validated_data)
        print('after create')
        for doc in documents_id_data:
            print('in loop ', dict(doc))
            document = Document.objects.get(pk=doc['pk'])  # так он называется в  document set
            task.document_set.add(document)
        return task



class TaskShortSerializer(serializers.HyperlinkedModelSerializer):

    user_to = UserShortSerializer(many=False, read_only=True)
    sys_user_add = UserShortSerializer(many=False, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'date', 'user_to', 'sys_date_add', 'sys_user_add']


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    type = DocumentTypeSerializer(many=False, read_only=True)
    type_name = serializers.CharField(source='type.name')
    counterpart = CounterpartSerializer(many=True, read_only=True)
    classifier = ClassifierSerializer(many=True, read_only=True)
    Tasks = TaskShortSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'type', 'type_name', 'nom', 'date', 'counterpart', 'description', 'classifier', 'Tasks', 'classifiers', 'counterparts']















