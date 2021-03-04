from rest_framework import viewsets
from rest_framework.response import Response

from .models import Insurer, RiskType, RiskField
from .serializers import (
    InsurerSerializer,
    RiskTypeSerializer,
    RiskFieldSerializer,
)


class InsurerViewSet(viewsets.ModelViewSet):

    queryset = Insurer.objects.all()
    serializer_class = InsurerSerializer


class RiskTypeViewSet(viewsets.ModelViewSet):

    queryset = RiskType.objects.all()
    serializer_class = RiskTypeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset)
        result = list()
        for obj in queryset:
            result.append(obj.describe())
        return Response(result)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        fields = RiskField.objects.filter(risk_type=instance.uid)
        serializer = self.get_serializer(instance)
        data = dict(serializer.data)
        fields_data = [field.describe() for field in fields]
        data["fields"] = fields_data
        return Response(data)


class RiskFieldViewSet(viewsets.ModelViewSet):

    queryset = RiskField.objects.all()
    serializer_class = RiskFieldSerializer


"""
class RiskViewSet(viewsets.ModelViewSet):

    queryset = Risk.objects.all()
    serializer_class = RiskSerializer
"""
