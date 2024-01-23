# Django
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator

# DRF
from rest_framework import status

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Local
from community.utils.api.response import Response


@method_decorator(name='create', decorator=swagger_auto_schema(operation_id=_('생성')))
class CreateModelMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(
                status=status.HTTP_201_CREATED,
                code=201,
                message='ok',
                data=serializer.data
            )

    def perform_create(self, serializer):
        return serializer.save()


@method_decorator(name='list', decorator=swagger_auto_schema(operation_id=_('리스트 조회')))
class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=serializer.data
        )


@method_decorator(name="retrieve", decorator=swagger_auto_schema(operation_id=_('객체 조회')))
class RetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=serializer.data
        )


@method_decorator(name="partial_update", decorator=swagger_auto_schema(operation_id=_('수정')))
class UpdateModelMixin(object):
    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=serializer.data
        )

    def perform_update(self, serializer):
        serializer.save()


@method_decorator(name="destroy", decorator=swagger_auto_schema(operation_id=_('삭제')))
class DestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            code=204,
            message='ok',
        )

    def perform_destroy(self, instance):
        instance.soft_delete()
