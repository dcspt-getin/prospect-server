from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
# from tagging.fields import TagField
from filer.fields.image import FilerImageField
from tinymce.models import HTMLField
import reversion

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
    ('PAIRWISE_COMBINATIONS', 'Combionações par a par'),
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


def input_label_default_value():
    return {"content": "", "position": "right"}


class Configuration(models.Model):
    key = models.CharField(max_length=60, blank=False, unique=True, null=False)
    value = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.key

    class Meta:
        permissions = ()


class Translation(models.Model):
    language = models.CharField(max_length=256, blank=False, null=False)
    language_code = models.CharField(max_length=256, blank=False, null=False)
    translations = models.JSONField(blank=True, null=True)


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


class Question(models.Model):
    groups = models.ManyToManyField(GroupQuestions)
    parent_question = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)

    rank = models.FloatField(blank=True, null=True)
    key = models.CharField(max_length=60, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    description_html = HTMLField(blank=True, null=True)
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
    value_min = models.CharField(max_length=60, blank=True, null=True)
    value_max = models.CharField(max_length=60, blank=True, null=True)
    checkbox_min_options = models.IntegerField(blank=True, null=True)
    checkbox_max_options = models.IntegerField(blank=True, null=True)
    value_interval = models.CharField(
        max_length=60, blank=True, null=True, default='1')
    show_previous_iteration = models.BooleanField(default=False)

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
        return self.title

    class Meta:
        permissions = ()
        ordering = ['row_order']


@reversion.register()
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_data = models.JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
