from rest_framework import status
from rest_framework.test import APITestCase
from .models import Insurer, RiskType, RiskField


class Tests(APITestCase):
    def test_flow(self):
        """
        Tests insurer, risks types and risks fields
        """

        url = "/api/insurers/"
        data = {"name": "Thanos Insurance"}
        response = self.client.post(url, data, format="json")
        insurer_uid = response.data["uid"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Insurer.objects.get(pk=insurer_uid).name, "Thanos Insurance")

        # Tests risktype
        url = "/api/risktype/"
        data = {
            "risk_name": "Cyber Risks",
            "description": "Insurance for homes",
            "insurer": response.data["uid"],
        }
        response = self.client.post(url, data, format="json")
        risktype1_uid = response.data["uid"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            RiskType.objects.get(pk=risktype1_uid).risk_name, "Cyber Risks"
        )

        data = {
            "risk_name": "Cyber Risks 2",
            "description": "Insurance for homes",
            "insurer": insurer_uid,
        }
        response = self.client.post(url, data, format="json")
        risktype2_uid = response.data["uid"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            RiskType.objects.get(pk=risktype2_uid).risk_name, "Cyber Risks 2"
        )

        # Tests duplicate name for risk type for a particular insurer
        # Should not allow
        data = {
            "risk_name": "Cyber Risks 2",
            "description": "Insurance for homes",
            "insurer": insurer_uid,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Tests Riskfield
        url = "/api/riskfield/"
        data = {
            "field_name": "sex",
            "field_type": "enum",
            "description": "gender of owner",
            "enum_constants": "male, female",
            "risk_type": risktype1_uid,
        }
        response = self.client.post(url, data, format="json")
        riskfield1_uid = response.data["uid"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RiskField.objects.get(pk=riskfield1_uid).field_name, "sex")
        self.assertEqual(RiskField.objects.get(pk=riskfield1_uid).field_type, "enum")
        self.assertEqual(
            RiskField.objects.get(pk=riskfield1_uid).enum_constants, "male, female"
        )
        # Get all risktypes
        url = "/api/riskfield/"
        data = {
            "field_name": "address",
            "field_type": "text",
            "description": "Address of risk",
            "risk_type": risktype2_uid,
        }
        response = self.client.post(url, data, format="json")
        riskfield2_uid = response.data["uid"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RiskField.objects.get(pk=riskfield2_uid).field_name, "address")
        self.assertEqual(RiskField.objects.get(pk=riskfield2_uid).field_type, "text")

        # Test get all risktypes
        url = "/api/risktype/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RiskType.objects.count(), 2)
