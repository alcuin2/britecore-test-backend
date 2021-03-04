from django.urls import path, include
from rest_framework.routers import DefaultRouter
from insurer import views

router = DefaultRouter()
router.register(r"insurers", views.InsurerViewSet)
router.register(r"risktype", views.RiskTypeViewSet)
router.register(r"riskfield", views.RiskFieldViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
