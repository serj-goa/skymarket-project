from django.urls import include, path
from rest_framework import routers

from .views import AdViewSet, CommentViewSet


ad_router = routers.SimpleRouter()
ad_router.register('', AdViewSet)

urlpatterns = [
    path('<int:ad_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:ad_pk>/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'})),
]

urlpatterns += ad_router.urls
