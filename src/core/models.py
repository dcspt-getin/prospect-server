from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
# from tagging.fields import TagField
from filer.fields.image import FilerImageField
from housearch.models import TerritorialUnitImage
from tinymce.models import HTMLField
import reversion

DEFAULT_USER_GROUP_KEY = "DEFAULT_USER_GROUP"

ACTIVE = 'ACTIVE'
NOT_ACTIVE = 'NOT_ACTIVE'
STATUS_CHOICES = [
    (ACTIVE, 'Ativa'),
    (NOT_ACTIVE, 'Desativa'),
]

QUESTION_TYPE_CHOICES = [
    ('ONLY_QUESTION_INFO', 'Somente informação'),
    ('MULTIPLE_CHOICE', 'Escolha múltipla'),
    ('SHORT_ANSWER', 'Resposta curta'),
    ('PAIRWISE_COMBINATIONS', 'Combinações par a par'),
    ('IMAGE_PAIRWISE_COMBINATIONS', 'Combinações de imagens par a par'),
    ('CITIZEN_PROFILE', 'Citizen Profile'),
    ('TERRITORIAL_COVERAGE', 'Escolha de cobertura territorial'),
    ('GEOLOCATION', 'Escolha de Geolocalização'),
    ('EMBEDDED_QUESTION', 'Embedded'),
]

INPUT_TYPE_CHOICES = [
    ('NUMBER', 'Number'),
    ('TEXT', 'Text'),
    ('SLIDER', 'Slider'),
]

MULTIPLE_SELECTION_TYPE_CHOICES = [
    ('RADIO', 'Radio'),
    ('SELECT', 'Select'),
    ('MULTIPLE_VALUES', 'Multiple'),
]

IMAGE_PAIRWISE_COMBINATIONS_TYPES = [
    ('BINARY_CHOICE', 'Escolha Binária'),
    ('WEIGHT_BASED_CHOICE', 'Escolha com base em pesos'),
]

LOCAL_SESSION = 'LOCAL_SESSION'
PROLIFIC = 'PROLIFIC'
USER_INTEGRATION_TYPES = [
    (LOCAL_SESSION, 'Local Session'),
    (PROLIFIC, 'Prolific'),
]


def input_label_default_value():
    return {"content": "", "position": "right"}


def slider_label_default_value():
    return {"right": "", "left": ""}


class Configuration(models.Model):
    key = models.CharField(max_length=60, blank=False, unique=True, null=False)
    value = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.key

    class Meta:
        permissions = ()
        verbose_name = 'Global Configuration'
        verbose_name_plural = 'Global Configurations'


class Translation(models.Model):
    language = models.CharField(max_length=256, blank=False, null=False)
    language_code = models.CharField(max_length=256, blank=False, null=False)
    translations = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.language


class GroupQuestions(models.Model):
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    user_group = models.ManyToManyField(Group, blank=True)

    name = models.CharField(max_length=256, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    visible_after = models.DateTimeField(blank=True, null=True)
    visible_before = models.DateTimeField(blank=True, null=True)
    is_visible_on_results = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        permissions = ()
        verbose_name = 'Group of Questions'
        verbose_name_plural = 'Groups of Questions'


class Question(models.Model):
    groups = models.ManyToManyField(GroupQuestions)
    parent_question = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)

    language = models.ForeignKey(
        Translation, on_delete=models.CASCADE, blank=True, null=True)
    territorial_unit_image = models.ForeignKey(
        TerritorialUnitImage, on_delete=models.CASCADE, related_name='territorial_unit_images', blank=True, null=True)
    rank = models.FloatField(blank=True, null=True)
    key = models.CharField(max_length=60, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    description_html = HTMLField(blank=True, null=True)
    help = HTMLField(blank=True, null=True)
    description_image = FilerImageField(blank=True, null=True,
                                        related_name="question_image", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=60, blank=True)
    question_type = models.CharField(
        max_length=60,
        choices=QUESTION_TYPE_CHOICES,
        default=None,
        blank=False,
        null=False
    )
    default_value = models.CharField(max_length=256, blank=True)
    correct_value = models.CharField(max_length=256, blank=True)
    input_type = models.CharField(
        max_length=30,
        choices=INPUT_TYPE_CHOICES,
        default=None,
        blank=True
    )
    input_size = models.CharField(max_length=56, blank=True, default="16")
    input_label = models.JSONField(
        blank=True, null=True, default=input_label_default_value)
    multiple_selection_type = models.CharField(
        max_length=30,
        choices=MULTIPLE_SELECTION_TYPE_CHOICES,
        default=None,
        blank=True
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
    image_pairwise_type = models.CharField(
        max_length=30,
        choices=IMAGE_PAIRWISE_COMBINATIONS_TYPES,
        default=None,
        blank=True,
        null=True
    )
    value_min = models.CharField(max_length=60, blank=True, null=True)
    value_max = models.CharField(max_length=60, blank=True, null=True)
    min_chars = models.CharField(max_length=60, blank=True, null=True)
    max_chars = models.CharField(max_length=60, blank=True, null=True)
    checkbox_min_options = models.IntegerField(blank=True, null=True)
    checkbox_max_options = models.IntegerField(blank=True, null=True)
    value_interval = models.CharField(
        max_length=60, blank=True, null=True, default='1')
    show_previous_iteration = models.BooleanField(default=False)
    is_required = models.BooleanField(default=True)
    show_balance = models.BooleanField(
        default=True, verbose_name="Show balance (If applicable)")
    territorial_coverages = models.CharField(
        max_length=60, blank=True, null=True, verbose_name="Territorial coverages (ids separated by comma)")
    use_google_street_images = models.BooleanField(
        default=False, verbose_name="Show Google Street Images")
    use_360_image = models.BooleanField(
        default=False, verbose_name="Show 360 Image")
    show_only_on_parent_value = models.CharField(
        max_length=60, blank=True, null=True, verbose_name="Show only if parent value is equals (values separated with commas)")
    slider_label = models.JSONField(
        blank=True, null=True, default=slider_label_default_value)
    disabled_after_filled = models.BooleanField(
        default=True, verbose_name="Disabled after filled")
    option_to_finish = models.CharField(
        max_length=60, blank=True, null=True, default='', verbose_name="Option id to send user to the end")
    embedded_question_url = models.CharField(
        max_length=268, blank=True, null=True, verbose_name="Embeded Question External Url")
    embedded_size = models.JSONField(
        blank=True, null=True, default={})

    def __str__(self):
        return "%s - %s" % (self.id, self.key)

    def get_children(self):
        return Question.objects.filter(parent_question=self, status=ACTIVE)

    class Meta:
        permissions = ()
        ordering = ['rank', '-id']


class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options')

    row_order = models.IntegerField(blank=False, null=False, default=0)
    title = models.CharField(max_length=256, blank=False, null=False)
    description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return "ID - %s" % (self.id)

    class Meta:
        permissions = ()
        ordering = ['row_order']


@reversion.register()
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_data = models.JSONField(blank=True, null=True, default={})
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    class Meta:
        permissions = ()
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            default_group_configuration = Configuration.objects.get(
                key=DEFAULT_USER_GROUP_KEY)

            if default_group_configuration and default_group_configuration.value:
                groups = Group.objects.filter(
                    pk__in=default_group_configuration.value.split(','))

                for group in groups:
                    instance.groups.add(group)

            UserProfile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()


class UserIntegration(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='users')

    type = models.CharField(
        max_length=30,
        choices=USER_INTEGRATION_TYPES,
        default='',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    meta = models.JSONField(blank=True, null=True)

    class Meta:
        permissions = ()
        verbose_name = 'User Integration'
        verbose_name_plural = 'User Integrations'


class Page(models.Model):
    language = models.ForeignKey(
        Translation, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug = models.CharField(max_length=60, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    header_menu = models.BooleanField(
        default=False, verbose_name="Visible on header menu")
    is_homepage = models.BooleanField(
        default=False, verbose_name="Is homepage")

    class Meta:
        permissions = ()
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
