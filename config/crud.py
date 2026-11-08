"""Shared helpers so every finance page (list + add + edit + delete) works the same way.

Every page:
  * requires login,
  * only ever shows/changes records that belong to request.user,
  * adds/edits records through a ModelForm that stamps the user and limits
    category/account choices to the user's own records.
"""
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View


def money(value):
    return f"₦{value:,.2f}"


def date_widget():
    return forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")


class OwnedModelForm(forms.ModelForm):
    """ModelForm for models that have a `user` foreign key."""

    owned_fields = ()  # FK fields whose choices are limited to the user's own records

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.instance.user = user  # set before validation so model.clean() can compare owners
        for name in self.owned_fields:
            field = self.fields[name]
            field.queryset = field.queryset.filter(user=user)

    def _get_validation_exclusions(self):
        # `user` is not a form field, but we want model validation (and unique
        # constraints that include `user`) to run with it.
        exclude = super()._get_validation_exclusions()
        exclude.discard("user")
        return exclude


class OwnedListCreateView(LoginRequiredMixin, View):
    """List page with an add/edit form. The page's own template (the instructor's design)
    receives: `form`, `editing`, `list_url` and the records under `context_name`."""

    model = None
    form_class = None
    template_name = None
    page = ""                # also the url namespace, e.g. "expenses"
    singular = ""
    context_name = "objects"
    select_related = ()
    order_by = ()

    def get_queryset(self, request):
        queryset = self.model.objects.filter(user=request.user)
        if self.select_related:
            queryset = queryset.select_related(*self.select_related)
        if self.order_by:
            queryset = queryset.order_by(*self.order_by)
        return queryset

    def prepare(self, request, objects):
        """Hook: add extra attributes to objects before they are shown."""
        return objects

    def get_instance(self, request, pk):
        if pk is None:
            return None
        return get_object_or_404(self.model, pk=pk, user=request.user)

    def render_page(self, request, form, instance):
        objects = self.prepare(request, list(self.get_queryset(request)))
        context = {
            "page": self.page,
            "form": form,
            "editing": instance is not None,
            "list_url": reverse(f"{self.page}:list"),
            self.context_name: objects,
        }
        return render(request, self.template_name, context)

    def get(self, request, pk=None):
        instance = self.get_instance(request, pk)
        form = self.form_class(instance=instance, user=request.user) if self.form_class else None
        return self.render_page(request, form, instance)

    def post(self, request, pk=None):
        if not self.form_class:
            return redirect(reverse(f"{self.page}:list"))
        instance = self.get_instance(request, pk)
        form = self.form_class(request.POST, instance=instance, user=request.user)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
            except ValidationError as error:
                form.add_error(None, ValidationError(error.messages))
            except IntegrityError:
                form.add_error(None, "That record conflicts with an existing one.")
            else:
                verb = "updated" if instance else "added"
                messages.success(request, f"{self.singular.capitalize()} {verb}.")
                return redirect(reverse(f"{self.page}:list"))
        return self.render_page(request, form, instance)


class OwnedDeleteView(LoginRequiredMixin, View):
    model = None
    success_url_name = ""
    singular = "record"

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, user=request.user)
        try:
            obj.delete()
        except (RestrictedError, ProtectedError):
            messages.error(
                request,
                f"This {self.singular} is still used by other records, so it can't be deleted.",
            )
        else:
            messages.success(request, f"{self.singular.capitalize()} deleted.")
        return redirect(self.success_url_name)