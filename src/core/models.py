from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
# from tagging.fields import TagField

ACTIVE = 'ACTIVE'
NOT_ACTIVE = 'NOT_ACTIVE'
STATUS_CHOICES = [
    (ACTIVE, 'Ativada'),
    (NOT_ACTIVE, 'Desativada'),
]

QUESTION_TYPE_CHOICES = [
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
]


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


class Question(models.Model):
    key = models.CharField(max_length=60, blank=True, null=True)
    title = models.CharField(max_length=256, blank=False, null=False)
    description = models.CharField(max_length=256, blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    image_url = models.CharField(max_length=60, blank=True)
    question_type = models.CharField(
        max_length=60,
        choices=QUESTION_TYPE_CHOICES,
        default=None,
        blank=False,
        null=False
    )
    default_value = models.CharField(max_length=256, blank=True)
    input_type = models.CharField(
        max_length=30,
        choices=INPUT_TYPE_CHOICES,
        default=None,
        blank=True
    )
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

    def __str__(self):
        return self.title

    class Meta:
        permissions = ()


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
