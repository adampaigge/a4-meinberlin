import django_filters
from django.apps import apps
from django.conf import settings
from django.utils.translation import ugettext as _

from adhocracy4.contrib.views import FilteredListView
from adhocracy4.projects import models as project_models

from apps.contrib.widgets import DropdownLinkWidget


class OrderingWidget(DropdownLinkWidget):
    label = _('Ordering')
    right = True


class OrganisationWidget(DropdownLinkWidget):
    label = _('Organisation')


class ProjectFilterSet(django_filters.FilterSet):

    ordering = django_filters.OrderingFilter(
        choices=(
            ('-created', _('Most recent')),
        ),
        empty_label=None,
        widget=OrderingWidget,
    )

    organisation = django_filters.ModelChoiceFilter(
        queryset=apps.get_model(settings.A4_ORGANISATIONS_MODEL).objects.all(),
        widget=OrganisationWidget,
    )

    class Meta:
        model = project_models.Project
        fields = ['organisation']


class ProjectListView(FilteredListView):
    model = project_models.Project
    paginate_by = 16
    filter_set = ProjectFilterSet
