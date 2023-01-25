from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Ad, Comment
from .permissions import IsAdminOrUser
from .serializers import AdDetailSerializer, AdSerializer, CommentSerializer
from .filters import AdFilter


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.select_related('author').all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = AdFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create', 'update', 'destroy'):
            return AdDetailSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        permission_classes = (AllowAny, )

        if self.action == 'retrieve':
            permission_classes = (IsAuthenticated, )

        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'me']:
            permission_classes = (IsAdminOrUser, )

        return tuple(permission() for permission in permission_classes)

    @action(detail=False, methods=('get', ))
    def me(self, request, *args, **kwargs):
        self.queryset = Ad.objects.filter(author=self.request.user).all()
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author').all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.select_related('author').select_related('ad').filter(ad__id=self.kwargs['ad_pk'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            ad=get_object_or_404(Ad, id=self.kwargs['ad_pk'])
        )

    def get_permissions(self):
        permission_classes = (IsAuthenticated, )

        if self.action in ['retrieve', 'list']:
            permission_classes = (IsAuthenticated, )

        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = (IsAdminOrUser, )

        return tuple(permission() for permission in permission_classes)
