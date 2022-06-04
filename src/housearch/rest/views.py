from rest_framework import viewsets
from rest_framework import permissions
from django_filters import rest_framework as filters
from rest_framework.permissions import DjangoModelPermissions

from .serializers import TerritorialCoverageSerializer, TerritorialUnitSerializer
from housearch.models import TerritorialCoverage, TerritorialUnit


class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['POST'] = ['%(app_label)s.add_%(model_name)s']
        self.perms_map['PUT'] = ['%(app_label)s.change_%(model_name)s']
        self.perms_map['DELETE'] = ['%(app_label)s.delete_%(model_name)s']


# ViewSets define the view behavior.
class TerritorialCoverageViewSet(viewsets.ModelViewSet):
    queryset = TerritorialCoverage.objects.all()
    serializer_class = TerritorialCoverageSerializer
    permission_classes = [permissions.IsAuthenticated,
                          CustomDjangoModelPermissions]


class TerritorialUnitViewSet(viewsets.ModelViewSet):
    queryset = TerritorialUnit.objects.all()
    serializer_class = TerritorialUnitSerializer
    permission_classes = [permissions.IsAuthenticated,
                          CustomDjangoModelPermissions]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'id': ["in", "exact"],  # note the 'in' field
    }
