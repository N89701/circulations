from django.urls import include, path
from rest_framework.routers import DefaultRouter


router_v1 = DefaultRouter()
# router_v1.register('organizations', OrganizationViewSet, basename='organizations')


urlpatterns = [
    path('', include(router_v1.urls)),
]