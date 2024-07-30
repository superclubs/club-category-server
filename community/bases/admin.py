from django.apps import apps
from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.forms import Textarea
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_admin_relation_links import AdminChangeLinksMixin
from django_reverse_admin import ReverseModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from inline_actions.admin import InlineActionsModelAdminMixin
from nested_inline.admin import NestedModelAdmin
from rangefilter.filter import DateRangeFilter

# 어드민 사이트 기본 앱 숨기기
for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        if admin.site.is_registered(model):
            admin.site.unregister(model)


def _related_field(model, lookup):
    names = lookup.split("__")
    boolean = False
    for name in names[:-1]:
        model = model._meta.get_field(name).remote_field.model
    try:
        verbose_name = model._meta.get_field(names[-1]).verbose_name
    except FieldDoesNotExist:
        property = getattr(model, names[-1])
        property = getattr(property, "fget", property)
        verbose_name = getattr(property, "short_description", names[-1])
        boolean = getattr(property, "boolean", False)

    def value(instance):
        for name in names[:-1]:
            instance = getattr(instance, name)
        if instance:
            return getattr(instance, names[-1])
        else:
            return None

    value.short_description = verbose_name
    value.boolean = boolean
    return value


class RelatedFieldAdminMixin:
    def __getattr__(self, name):
        if "__" in name:
            return _related_field(self.model, name)
        return super().__getattr__(name)


def extend_fields(fields, front_fields=[], back_fields=[]):
    if type(fields) is list:
        return list(front_fields) + fields + list(back_fields)
    elif type(fields) is tuple:
        return tuple(front_fields) + fields + tuple(back_fields)
    else:
        return fields


class InlineActionsModelAdminMixin(InlineActionsModelAdminMixin):
    InlineActionsModelAdminMixin.render_inline_actions.short_description = _("부가 기능")


class Admin(
    NestedModelAdmin,
    InlineActionsModelAdminMixin,
    ImportExportModelAdmin,
    AdminChangeLinksMixin,
    RelatedFieldAdminMixin,
    ReverseModelAdmin,
    SummernoteModelAdmin,
):
    list_filter = (("created", DateRangeFilter),)
    list_per_page = 10
    resource_class = resources.ModelResource

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "style": "width: 70%;"})},
    }

    # django-reverse-admin
    inline_type = "tabular"
    inline_reverse = ()

    def get_created(self, obj):
        if obj and obj.created:
            return obj.created.date()
        else:
            return None

    get_created.admin_order_field = "created"
    get_created.short_description = "생성일"

    def get_modified(self, obj):
        if obj and obj.created:
            return obj.created.date()
        else:
            return None

    get_modified.admin_order_field = "modified"
    get_modified.short_description = "수정일"

    def get_list_display(self, request):
        fields = super().get_list_display(request)
        return extend_fields(fields=fields, front_fields=["id"], back_fields=["get_created", "get_modified"])

    def get_list_display_links(self, request, list_display):
        fields = super().get_list_display_links(request, list_display)
        return extend_fields(fields=fields, front_fields=["id"], back_fields=["get_created", "get_modified"])

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request)
        return extend_fields(fields=fields, front_fields=["id"], back_fields=["created", "modified"])

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request)
        return extend_fields(fields=fields, front_fields=["id"], back_fields=["created", "modified"])


class CountAdmin(Admin):
    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=...) -> bool:
        return True

    def has_change_permission(self, request: HttpRequest, obj=...) -> bool:
        return False
