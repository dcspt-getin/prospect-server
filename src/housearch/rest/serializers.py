from rest_framework import serializers
from housearch.models import TerritorialCoverage, TerritorialUnit, \
    TerritorialUnitImage
from django.utils.translation import gettext_lazy as _


class TerritorialUnitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerritorialUnitImage
        fields = ['id', 'name', 'image', 'image_url', 'geometry']


class TerritorialUnitSerializer(serializers.ModelSerializer):
    images = TerritorialUnitImageSerializer(many=True, read_only=True)

    class Meta:
        model = TerritorialUnit
        fields = ['id', 'name', 'tucode', 'images',
                  'geometry', 'properties', 'status']


class TerritorialCoverageSerializer(serializers.ModelSerializer):
    units = TerritorialUnitSerializer(many=True, read_only=True)

    class Meta:
        model = TerritorialCoverage
        fields = ['id', 'units', 'name', 'municod', 'aditional_data', 'status']
