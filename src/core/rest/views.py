import math
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from django_filters import rest_framework as filters
from rest_framework.permissions import DjangoModelPermissions
from datetime import datetime
import pandas as pd
import numpy as np
from django.db.models import Q
from django.utils import timezone

from .serializers import QuestionSerializer, TranslationSerializer, UserProfileSerializer, UserSerializer, \
    MyTokenObtainSerializer, ConfigurationSerializer, GroupQuestionSerializer, PageSerializer
from core.models import ACTIVE, Configuration, GroupQuestions, Question, Translation, UserProfile, UserIntegration, USER_INTEGRATION_TYPES, Page


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

    @action(detail=False, methods=['post'])
    def calc_correl(self, request):
        l = request.data['xarr']
        M1 = pd.DataFrame(l)

        l2 = request.data['yarr']
        M2 = pd.DataFrame(l2)

        a1 = M1.to_numpy()
        a1 = a1.flatten()
        a2 = M2.to_numpy()
        a2 = a2.flatten()

        result = np.corrcoef(a1, a2)
        result = result[1][0]

        if math.isnan(result):
            result = 1

        return Response({'result': result})


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

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = GroupQuestions.objects.all()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'results': serializer.data,
        })


class QuestionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'id': ["in", "exact"],
        'question_type': ["in", "exact"],
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        user_questions_groups = GroupQuestions.objects.filter(visible_after__lte=datetime.now(), visible_before__gte=datetime.now(),
                                                              user_group__in=self.request.user.groups.all())

        return self.queryset.filter(groups__in=user_questions_groups, status=ACTIVE)

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = Question.objects.all()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'results': serializer.data,
        })


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

    @action(detail=False, methods=['get'])
    def results(self, request):
        group = request.query_params.get('group', None)
        questions_groups = GroupQuestions.objects.filter(id=group)
        questions = Question.objects.filter(groups__in=questions_groups)
        queryset = UserProfile.objects.all()
        filters = []

        for question in questions:
            filters.append(Q(profile_data__has_key=str(question.id)))

        query = filters.pop()

        # Or the Q object with the ones remaining in the list
        for item in filters:
            query |= item

        queryset = queryset.filter(query)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class UserIntegrationsView(APIView):
    permission_classes = []
    http_method_names = ['post']

    def post(self, request):
        data = request.data
        type = data.get('type')
        session_id = data.get('session_id')
        user_group = data.get('user_group')
        data = data.get('data', {})

        # Body validations
        if not type:
            return Response('type is required')
        if not session_id:
            return Response('session_id is required')
        if not user_group:
            return Response('user_group is required')
        if not dict(USER_INTEGRATION_TYPES).get(type):
            return Response('type is not allowed')

        user_integration = None

        # Check if user integration already exists
        try:
            user_integration = UserIntegration.objects.get(
                type=type, meta__session_id=session_id, meta__user_group=user_group)
        except UserIntegration.DoesNotExist:
            # handle the exception
            print('user_integration not exists')

        # if not exists
        #    1. create new Anonymous user
        #    2. Associate the user with session questions group
        #    3. Create new user integration for created user
        if not user_integration:
            meta = {
                'session_id': session_id,
                'user_group': user_group,
            }

            if data:
                meta.update(data)

            user = User.objects.create(
                username='Anonymous User %s' % get_random_string(length=32))
            user.groups.clear()

            user_questions_groups = GroupQuestions.objects.filter(
                pk=user_group)
            for user_question_group in user_questions_groups:
                for group in user_question_group.user_group.all():
                    user.groups.add(group)

            try:
                user_integration = UserIntegration.objects.create(
                    type=type, meta=meta, user=user)
            except:
                user.delete()

                return Response('Failed to create user integration')

        serializer = MyTokenObtainSerializer(
            user_integration.user, context={'request': request})

        refresh = serializer.get_token(user_integration.user)

        user_integration.user.last_login = timezone.now()
        user_integration.user.save(update_fields=["last_login"])

        result = {}

        result['refresh'] = str(refresh)
        result['access'] = str(refresh.access_token)

        return Response(result)


class PagesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = []
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'language': ["exact"],
        'slug': ["exact"],
    }
