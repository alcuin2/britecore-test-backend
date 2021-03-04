from django.db import models


import uuid


FIELD_TYPES = (
    ("number", "number"),
    ("text", "text"),
    ("date", "date"),
    ("enum", "enum"),
)


class Insurer(models.Model):

    uid = models.CharField(
        max_length=50, default=uuid.uuid4, unique=True, primary_key=True,
    )

    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name.capitalize()


class RiskField(models.Model):

    uid = models.CharField(
        max_length=50, default=uuid.uuid4, unique=True, primary_key=True,
    )
    risk_type = models.CharField(max_length=100)
    field_name = models.CharField(max_length=50)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPES)
    enum_constants = models.CharField(max_length=256, blank=True)
    description = models.TextField(default="")

    def describe(self):
        description = dict()
        description["uid"] = self.uid
        description["risk_type"] = self.risk_type
        description["field_name"] = self.field_name
        description["field_type"] = self.field_type
        if self.field_type == "enum":
            description["enum_constants"] = self.enum_constants

        description["description"] = self.description
        return description

    def __str__(self):

        return f"{self.field_name} - {self.risk_type}"


class RiskType(models.Model):

    uid = models.CharField(
        max_length=50, default=uuid.uuid4, unique=True, primary_key=True,
    )

    insurer = models.ForeignKey(Insurer, on_delete=models.DO_NOTHING,)
    insurer_name = models.CharField(max_length=50, blank=True)
    risk_name = models.CharField(max_length=50)
    description = models.TextField(default="")

    def describe(self):
        fields = RiskField.objects.filter(risk_type=self.uid)
        description = dict()
        description["uid"] = self.uid
        description["insurer"] = self.insurer.uid
        description["insurer_name"] = self.insurer_name
        description["risk_name"] = self.risk_name
        description["description"] = self.description

        list_of_field_desc = list()
        for field in fields:
            list_of_field_desc.append(field.describe())
        description["fields"] = list_of_field_desc

        return description

    def __str__(self):
        return f"{self.risk_name} - {self.insurer}"


"""
class Risk(models.Model):

    uid = models.CharField(
        max_length=50, default=uuid.uuid4, unique=True, primary_key=True,
    )
    owner = models.CharField(
        max_length=200
    )  # Ideally, this should be a foreign key to a User class
    insurer = models.ForeignKey(Insurer, on_delete=models.DO_NOTHING,)
    risk_type = models.ForeignKey(RiskType, on_delete=models.DO_NOTHING,)

    def __str__(self):
        return f"{self.owner} - {self.risk_type}"

"""

