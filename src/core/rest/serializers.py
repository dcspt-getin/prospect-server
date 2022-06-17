
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from core.models import Configuration, GroupQuestions, Question, QuestionOption, Translation, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


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

        self.user.last_login = timezone.now()
        self.user.save(update_fields=["last_login"])

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
                  'first_name', 'last_name', 'groups', 'is_staff',)

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
        fields = ['id', 'name', 'description',
                  'parent', 'visible_after', 'visible_before', 'is_visible_on_results']

    def get_related_field(self, model_field):
        return GroupQuestionSerializer()


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'title', 'description', 'row_order']


class HTMLField(serializers.Field):
    def to_representation(self, value):
        return value


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)
    description_image = serializers.ImageField()
    description_html = HTMLField()
    parent_question = serializers.PrimaryKeyRelatedField(read_only=True)
    children = serializers.SerializerMethodField()
    groups = GroupQuestionSerializer(many=True, read_only=True)

    def get_children(self, obj):
        serializer = self.__class__(
            obj.get_children(), many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Question
        fields = ['id', 'key', 'rank', 'title', 'groups', 'parent_question', 'description', 'description_html', 'description_image', 'image_url', 'question_type',
                  'input_size', 'input_label', 'correct_value', 'default_value', 'value_min', 'value_max', 'value_interval', 'checkbox_min_options', 'checkbox_max_options',
                  'input_type', 'multiple_selection_type', 'status', 'options', 'children', 'show_previous_iteration', 'is_required']
