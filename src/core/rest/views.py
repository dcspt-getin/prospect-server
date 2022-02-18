from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from django_filters import rest_framework as filters
from rest_framework.permissions import DjangoModelPermissions

from .serializers import QuestionSerializer, TranslationSerializer, UserProfileSerializer, UserSerializer, MyTokenObtainSerializer, ConfigurationSerializer, GroupQuestionSerializer
from core.models import Configuration, GroupQuestions, Question, Translation, UserProfile


class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['POST'] = ['%(app_label)s.add_%(model_name)s']
        self.perms_map['PUT'] = ['%(app_label)s.change_%(model_name)s']
        self.perms_map['DELETE'] = ['%(app_label)s.delete_%(model_name)s']


class MyTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          CustomDjangoModelPermissions]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'groups__id': ["in"],
    }

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)

        return super(UserViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(id=self.request.user.id)


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        permissions = request.user.get_all_permissions()

        result = {'permissions': permissions}
        result.update(serializer.data)

        return Response(result)


class ConfigurationsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    permission_classes = []


class TranslationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Translation.objects.all()
    permission_classes = []
    serializer_class = TranslationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'language': ["exact"],
        'language_code': ["exact"],
    }


class GroupQuestionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GroupQuestions.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupQuestionSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = {
    #     'id': ["in", "exact"],
    #     'question_type': ["in", "exact"],
    # }


class QuestionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'id': ["in", "exact"],
        'question_type': ["in", "exact"],
    }


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super(UserProfileViewSet, self).perform_create(serializer)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)
