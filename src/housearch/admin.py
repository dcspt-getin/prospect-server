from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import TerritorialCoverage, TerritorialUnitImage, TerritorialUnit
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
from openpyxl import load_workbook
from django_json_widget.widgets import JSONEditorWidget

from .helpers import load_geo_json, import_territorial_unit_images_json


def import_action(self, request, import_method, *args, **kwargs):
    print('import_action')
    if not self.has_import_permission(request):
        raise PermissionDenied

    context = self.get_import_context_data()

    import_formats = self.get_import_formats()
    form_type = self.get_import_form()
    form_kwargs = self.get_form_kwargs(form_type, *args, **kwargs)
    form = form_type(import_formats,
                     request.POST or None,
                     request.FILES or None,
                     **form_kwargs)

    if request.POST and form.is_valid():
        input_format = import_formats[
            int(form.cleaned_data['input_format'])
        ]()
        import_file = form.cleaned_data['import_file']
        # first always write the uploaded file to disk as it may be a
        # memory file or else based on settings upload handlers
        tmp_storage = self.write_to_tmp_storage(import_file, input_format)

        # then read the file, using the proper format-specific mode
        # warning, big files may exceed memory
        try:
            data = tmp_storage.read(input_format.get_read_mode())
            # if not input_format.is_binary() and self.from_encoding:
            #     data = force_str(data, self.from_encoding)
        except UnicodeDecodeError as e:
            return HttpResponse(_(u"<h1>Imported file has a wrong encoding: %s</h1>" % e))
        except Exception as e:
            return HttpResponse(_(u"<h1>%s encountered while trying to read file: %s</h1>" % (type(e).__name__, import_file.name)))

        import_method(import_file, data)

        res_kwargs = self.get_import_resource_kwargs(
            request, form=form, *args, **kwargs)
        resource = self.get_import_resource_class()(**res_kwargs)
    else:
        res_kwargs = self.get_import_resource_kwargs(
            request, form=form, *args, **kwargs)
        resource = self.get_import_resource_class()(**res_kwargs)

    context.update(self.admin_site.each_context(request))

    context['title'] = _("Import")
    context['form'] = form
    context['opts'] = self.model._meta
    context['fields'] = self.import_fields

    request.current_app = self.admin_site.name
    return TemplateResponse(request, [self.import_template_name],
                            context)


@admin.register(TerritorialCoverage)
class TerritorialCoverageAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'name', 'municod', 'aditional_data', 'status')
    list_display = ('id', 'name',)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


class ImportTerritorialUnitImageAdmin(ImportMixin, admin.ModelAdmin):
    formats = [base_formats.JSON]
    import_fields = [
        'TUCod -> TerritorialUnit.tucode',
        'IMG_name -> name',
        'Image_url -> image_url',
        'Long_y -> geometry.lat',
        'Long_x -> geometry.lng',
    ]

    """
    Subclass of ModelAdmin with import/export functionality.
    """

    def import_action(self, request, *args, **kwargs):
        """
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        """

        def import_method(import_file, data):
            data = json.loads(data)

            import_territorial_unit_images_json(data)

        return import_action(self, request, import_method)


class TerritorialUnitImageResource(resources.ModelResource):
    class Meta:
        model = TerritorialUnitImage


@admin.register(TerritorialUnitImage)
class TerritorialUnitImageAdmin(ImportTerritorialUnitImageAdmin):
    resource_class = TerritorialUnitImageResource
    readonly_fields = ('id',)
    fields = ('id', 'name', 'image', 'image_url',
              'geometry', 'territorial_unit')
    list_display = ('name',)
    list_filter = ('territorial_unit',
                   'territorial_unit__territorial_coverage')
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


class TerritorialUnitResource(resources.ModelResource):
    class Meta:
        model = TerritorialUnit


class CustomImportForm(ImportForm):
    pass


class ImportTerritorialUnitAdmin(ImportMixin, admin.ModelAdmin):
    formats = [base_formats.JSON]
    import_fields = [
        'features[Array].properties.MUNICOD -> TerritorialCoverage.municod',
        'features[Array].properties.TUCod -> tucode',
        'features[Array].properties.name -> name',
        'features[Array].properties -> properties',
        'features[Array] -> geometry',
    ]

    """
    Subclass of ModelAdmin with import/export functionality.
    """

    def import_action(self, request, *args, **kwargs):
        """
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        """

        def import_method(import_file, data):
            data = json.loads(data)

            load_geo_json(data)

        return import_action(self, request, import_method)


@admin.register(TerritorialUnit)
class TerritorialUnitAdmin(ImportTerritorialUnitAdmin):
    resource_class = TerritorialUnitResource
    readonly_fields = ('id',)
    fields = ('id', 'name', 'tucode', 'geometry', 'properties',
              'territorial_coverage', 'tags', 'status')
    list_display = ('id', 'name', 'tucode',)
    list_filter = ('territorial_coverage', 'tags')
    search_fields = ('name',)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
