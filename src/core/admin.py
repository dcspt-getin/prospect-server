from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Translation, Configuration, Question, QuestionOption, UserProfile, GroupQuestions, Page, UserIntegration
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets
from import_export.admin import ImportMixin
from import_export.forms import ImportForm
from import_export.formats import base_formats
from django.db import models
from django.http import HttpResponse
import json
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from openpyxl import load_workbook
from django_json_widget.widgets import JSONEditorWidget
from reversion.admin import VersionAdmin
import nested_admin
from drfpasswordless.services import TokenService
from drfpasswordless.models import CallbackToken
from drfpasswordless.settings import api_settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django_admin_relation_links import AdminChangeLinksMixin


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class UserResource(resources.ModelResource):
    groups = fields.Field(
        column_name='group_name',
        attribute='groups',
        widget=widgets.ManyToManyWidget(Group, ',', 'name')
    )

    # def before_import_row(self, row, **kwargs):
    #     value = row['password']
    #     row['password'] = make_password(value)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'group_name')


def send_email(modeladmin, request, queryset):
    alias_type = 'email'
    token_type = CallbackToken.TOKEN_TYPE_AUTH
    email_subject = api_settings.PASSWORDLESS_EMAIL_SUBJECT
    email_plaintext = api_settings.PASSWORDLESS_EMAIL_PLAINTEXT_MESSAGE
    email_html = api_settings.PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE_NAME
    message_payload = {'email_subject': email_subject,
                       'email_plaintext': email_plaintext,
                       'email_html': email_html}
    for user in queryset:
        TokenService.send_token(
            user, alias_type, token_type, **message_payload)


send_email.short_description = 'Send email for user login'


class UserAdmin(ImportExportModelAdmin, UserAdmin):
    # list_filter = ('created_at',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    # fields = ('id', 'username', 'email', 'first_name',
    #           'last_name', 'is_staff', 'is_active', 'is_superuser', 'groups', 'date_joined', 'last_login')
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    resource_class = UserResource
    actions = [send_email]
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    # list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser",
                   "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

GroupAdmin.list_display = ('id', 'name')


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'key', 'value')
    list_display = ('id', 'key', 'value')


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'language', 'language_code', 'translations')
    list_display = ('id', 'language', 'language_code')
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(GroupQuestions)
class GroupQuestionsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'parent', 'user_group', 'name', 'visible_after',
              'visible_before', 'is_visible_on_results', 'description')
    list_display = ('id', 'name', 'parent', 'visible_after', 'visible_before')
    list_filter = ('parent', 'user_group')


class QuestionOptionInline(nested_admin.SortableHiddenMixin, nested_admin.NestedTabularInline):
    model = QuestionOption
    sortable_field_name = "row_order"
    fields = ('title', 'description', 'row_order')
    extra = 0


@admin.register(Question)
class QuestionAdmin(nested_admin.NestedModelAdmin):
    readonly_fields = ('id',)
    fieldsets = (
        (None, {
            'fields': ('id', 'rank', 'key', 'language', 'status', 'groups',
                       'parent_question', 'title', 'description', 'description_html', 'help',
                       'correct_value', 'is_required', 'show_balance', 'show_only_on_parent_value', 'question_type', 'disabled_after_filled'),
        }),
        ('Imagem', {
            'fields': ('description_image', 'image_url', 'territorial_unit_image', 'use_google_street_images', 'use_360_image'),
            'classes': ('collapse',),
        }),
        ('Opções de Resposta Curta', {
            'fields': ('input_type',
                       'input_size', 'input_label', 'slider_label', 'default_value', 'value_interval', 'value_min', 'value_max', 'min_chars', 'max_chars'),
            'classes': ('collapse',),
        }),
        ('Opções de Escolha multipla', {
            'fields': ('multiple_selection_type', 'checkbox_min_options', 'checkbox_max_options', 'option_to_finish'),
            'classes': ('collapse',),
        }),
        ('Opções de Combinações par a par', {
            'fields': ('show_previous_iteration',),
            'classes': ('collapse',),
        }),
        ('Opções de Combinações de imagens par a par', {
            'fields': ('image_pairwise_type', 'territorial_coverages'),
            'classes': ('collapse',),
        }),
    )
    list_display = ('id', 'rank', 'key', 'title', 'parent_question',
                    'status', 'language', 'question_groups', 'question_type')
    list_filter = ('groups', 'status', 'question_type', 'language')
    inlines = [QuestionOptionInline]
    save_as = True

    def question_groups(self, obj):
        return "\n".join([str(p) for p in obj.groups.all()])


@admin.register(UserProfile)
class UserProfileAdmin(VersionAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at',)
    fields = ('id', 'created_at', 'updated_at',
              'user', 'profile_data', 'status')
    list_display = ('id', 'user', 'status')
    list_filter = ('status', 'user')
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at',)
    fields = ('id', 'created_at', 'updated_at',
              'language', 'slug', 'header_menu', 'is_homepage', 'title', 'content')
    list_display = ('id', 'title', 'slug', 'language',
                    'header_menu', 'is_homepage')
    list_filter = ('language', 'header_menu', 'is_homepage')
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    save_as = True


@admin.register(UserIntegration)
class UserIntegrationAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at',)
    fields = ('id', 'created_at', 'updated_at',
              'type', 'user', 'meta')
    list_display = ('id', 'type', 'user_link')
    list_filter = ('type', 'user',)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    change_links = ['user']
