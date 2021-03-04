from rest_framework import serializers
from .models import Insurer, RiskType, RiskField


class InsurerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurer
        fields = "__all__"


class RiskTypeSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        risk_name = validated_data["risk_name"]
        insurer = validated_data["insurer"]
        if (
            RiskType.objects.filter(insurer=insurer, risk_name=risk_name).count() > 0
        ):  # Do not allow duplicate risk names
            raise serializers.ValidationError(
                f"Risk name '{risk_name}' already exists for insurer"
            )

        insurer_object = Insurer.objects.get(pk=insurer.uid)
        validated_data["insurer_name"] = insurer_object.name
        obj = RiskType.objects.create(**validated_data)
        obj.save()
        return obj

    class Meta:
        model = RiskType
        fields = "__all__"


class RiskFieldSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        field_name = validated_data["field_name"]
        risk_type = validated_data["risk_type"]
        if (
            RiskField.objects.filter(
                risk_type__iexact=risk_type, field_name__iexact=field_name
            ).count()
            > 0
        ):
            raise serializers.ValidationError(
                {
                    "detail": f"Risk field name with '{field_name}' already exists for risk type"
                }
            )

        if validated_data["field_type"] == "enum" and (
            validated_data.get("enum_constants") is None
            or validated_data.get("enum_constants") == ""
        ):
            raise serializers.ValidationError(
                {
                    "detail": "Enum field type must have at least one value for 'enum_constants'"
                }
            )

        obj = RiskField.objects.create(**validated_data)
        obj.save()
        return obj

    class Meta:
        model = RiskField
        fields = "__all__"


"""
class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = "__all__"
"""
