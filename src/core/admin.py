from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Translation, Configuration, Question, QuestionOption, UserProfile, GroupQuestions
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


# def import_action(self, request, import_method, *args, **kwargs):
#     print('import_action')
#     if not self.has_import_permission(request):
#         raise PermissionDenied

#     context = self.get_import_context_data()

#     import_formats = self.get_import_formats()
#     form_type = self.get_import_form()
#     form_kwargs = self.get_form_kwargs(form_type, *args, **kwargs)
#     form = form_type(import_formats,
#                         request.POST or None,
#                         request.FILES or None,
#                         **form_kwargs)

#     if request.POST and form.is_valid():
#         input_format = import_formats[
#             int(form.cleaned_data['input_format'])
#         ]()
#         import_file = form.cleaned_data['import_file']
#         # first always write the uploaded file to disk as it may be a
#         # memory file or else based on settings upload handlers
#         tmp_storage = self.write_to_tmp_storage(import_file, input_format)

#         # then read the file, using the proper format-specific mode
#         # warning, big files may exceed memory
#         try:
#             data = tmp_storage.read(input_format.get_read_mode())
#             # if not input_format.is_binary() and self.from_encoding:
#             #     data = force_str(data, self.from_encoding)
#         except UnicodeDecodeError as e:
#             return HttpResponse(_(u"<h1>Imported file has a wrong encoding: %s</h1>" % e))
#         except Exception as e:
#             return HttpResponse(_(u"<h1>%s encountered while trying to read file: %s</h1>" % (type(e).__name__, import_file.name)))

#         import_method(import_file, data)

#         res_kwargs = self.get_import_resource_kwargs(request, form=form, *args, **kwargs)
#         resource = self.get_import_resource_class()(**res_kwargs)
#     else:
#         res_kwargs = self.get_import_resource_kwargs(request, form=form, *args, **kwargs)
#         resource = self.get_import_resource_class()(**res_kwargs)

#     context.update(self.admin_site.each_context(request))

#     context['title'] = _("Import")
#     context['form'] = form
#     context['opts'] = self.model._meta
#     context['fields'] = self.import_fields

#     request.current_app = self.admin_site.name
#     return TemplateResponse(request, [self.import_template_name],
#                             context)


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
                       'parent_question', 'title', 'description', 'description_html', 'description_image', 'image_url',
                       'correct_value', 'is_required', 'show_balance', 'question_type'),
        }),
        ('Opções de Resposta Curta', {
            'fields': ('input_type',
                       'input_size', 'input_label', 'default_value', 'value_interval', 'value_min', 'value_max'),
            'classes': ('collapse',),
        }),
        ('Opções de Escolha multipla', {
            'fields': ('multiple_selection_type', 'checkbox_min_options', 'checkbox_max_options'),
            'classes': ('collapse',),
        }),
        ('Opções de Combinações par a par', {
            'fields': ('show_previous_iteration',),
            'classes': ('collapse',),
        }),
        ('Opções de Combinações de imagens par a par', {
            'fields': ('image_pairwise_type', 'territorial_coverages', 'use_google_street_images', 'use_360_image'),
            'classes': ('collapse',),
        }),
    )
    list_display = ('id', 'rank', 'key', 'title', 'parent_question',
                    'question_type', 'question_groups', 'status', 'language')
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
