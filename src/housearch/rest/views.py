from rest_framework import viewsets
from rest_framework import permissions
from django_filters import rest_framework as filters
from rest_framework.permissions import DjangoModelPermissions

from .serializers import TerritorialCoverageSerializer, TerritorialUnitSerializer
from housearch.models import TerritorialCoverage, TerritorialUnit


# ViewSets define the view behavior.
class TerritorialCoverageViewSet(viewsets.ModelViewSet):
    queryset = TerritorialCoverage.objects.all()
    serializer_class = TerritorialCoverageSerializer
    permission_classes = [permissions.IsAuthenticated]


class TerritorialUnitViewSet(viewsets.ModelViewSet):
    queryset = TerritorialUnit.objects.all()
    serializer_class = TerritorialUnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'id': ["in", "exact"],  # note the 'in' field
    }
