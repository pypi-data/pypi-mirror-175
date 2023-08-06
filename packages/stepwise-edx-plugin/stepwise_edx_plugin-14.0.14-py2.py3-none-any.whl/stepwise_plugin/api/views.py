from rest_framework import viewsets

# this repo
from stepwise_plugin.models import Configuration

# this module
from .serializers import ConfigurationSerializer


class ConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
