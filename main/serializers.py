from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Document, Comment, Member, User

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'project', 'name', 'file']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)  # добавляем сюда

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'owner', 'documents']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'project', 'user', 'text']


class MemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='member.id', read_only=True)
    username = serializers.CharField(source='member.username', read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ['id', 'username', 'is_owner']

    def get_is_owner(self, obj):
        return obj.project.owner_id == obj.member_id