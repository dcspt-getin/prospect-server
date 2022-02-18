
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from core.models import Configuration, GroupQuestions, Question, QuestionOption, Translation, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _


class MyTokenObtainSerializer(TokenObtainPairSerializer, TokenObtainSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            try:
                user_temp = get_user_model().objects.get(
                    username=attrs[self.username_field])
            except:
                user_temp = None

            if user_temp is not None and user_temp.is_active is False and user_temp.check_password(attrs['password']):
                raise exceptions.AuthenticationFailed(
                    'account_not_active',
                    'account_not_active',
                )
            else:
                raise exceptions.AuthenticationFailed(
                    self.error_messages['no_active_account'],
                    'no_active_account',
                )

        data = {}

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
    )
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'first_name', 'last_name', 'groups')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'created_at', 'updated_at',
                  'user_id', 'profile_data', 'status']


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['id', 'key', 'value', ]


class TranslationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Translation
        fields = ['id', 'language', 'language_code', 'translations']


class GroupQuestionSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GroupQuestions
        fields = ['id', 'name', 'description', 'parent']

    def get_related_field(self, model_field):
        return GroupQuestionSerializer()


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'title', 'description', 'row_order']


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)
    group = GroupQuestionSerializer(read_only=True)
    description_image = serializers.ImageField()

    class Meta:
        model = Question
        fields = ['id', 'key', 'title', 'group', 'description', 'description_image', 'image_url', 'question_type',
                  'default_value', 'value_min', 'value_max', 'input_type', 'multiple_selection_type', 'status', 'options']
