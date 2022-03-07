from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Translation, Configuration, Question, QuestionOption, UserProfile, GroupQuestions
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from import_export import resources
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


UserAdmin.list_display = (
    'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

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
class GroupQuestionsAdmin(nested_admin.NestedModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'parent', 'name', 'description')
    list_display = ('id', 'name', 'parent')
    list_filter = ('parent',)


class QuestionOptionInline(nested_admin.NestedTabularInline):
    model = QuestionOption
    sortable_field_name = "row_order"
    fields = ('title', 'description', 'row_order')
    extra = 0


@admin.register(Question)
class QuestionAdmin(nested_admin.NestedModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'rank', 'key', 'group', 'title', 'description', 'description_html', 'description_image', 'image_url', 'question_type', 'input_type',
              'default_value', 'value_min', 'value_max', 'value_interval', 'multiple_selection_type', 'status')
    list_display = ('id', 'rank', 'key', 'title',
                    'question_type', 'status', 'group')
    list_filter = ('group', 'status', 'question_type')
    inlines = [QuestionOptionInline]


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
