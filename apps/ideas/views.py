import django_filters
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views import generic

from adhocracy4.categories import models as category_models
from adhocracy4.contrib.views import FilteredListView
from adhocracy4.contrib.views import PermissionRequiredMixin
from adhocracy4.modules.models import Module
from adhocracy4.projects import mixins

from apps.contrib.mixins import ChoicesRequestMixin
from apps.contrib.widgets import DropdownLinkWidget

from . import models as idea_models
from . import forms


def category_queryset(request):
    return category_models.Category.objects.filter(module=request.module)


class OrderingWidget(DropdownLinkWidget):
    label = _('Ordering')
    right = True


class IdeaOrdering(ChoicesRequestMixin, django_filters.OrderingFilter):

    def get_choices(self, request):
        choices = (('-created', _('Most recent')),)
        if self.parent.request.module.has_feature('rate', idea_models.Idea):
            choices += ('-positive_rating_count', _('Most popular')),
        choices += ('-comment_count', _('Most commented')),
        return choices


class CategoryFilterWidget(DropdownLinkWidget):
    label = _('Category')


class IdeaFilterSet(django_filters.FilterSet):

    category = django_filters.ModelChoiceFilter(
        queryset=category_queryset,
        widget=CategoryFilterWidget,
    )

    ordering = IdeaOrdering(
        empty_label=None,
        widget=OrderingWidget,
    )

    @property
    def qs(self):
        return super().qs.filter(module=self.request.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()

    class Meta:
        model = idea_models.Idea
        fields = ['category']


class RequestMixin(object):
    """Add module information needed by filter to request object.

    Depends on attributes set by the ProjectMixin and must come after it in the
    dispatch order.
    """

    def dispatch(self, *args, **kwargs):
        self.request.module = self.module
        return super().dispatch(*args, **kwargs)


class IdeaListView(mixins.ProjectMixin, RequestMixin, FilteredListView):
    model = idea_models.Idea
    paginate_by = 15
    filter_set = IdeaFilterSet


class IdeaDetailView(PermissionRequiredMixin, generic.DetailView):
    model = idea_models.Idea
    queryset = idea_models.Idea.objects.annotate_positive_rating_count()\
                                       .annotate_negative_rating_count()
    permission_required = 'meinberlin_ideas.view_idea'


class IdeaCreateView(PermissionRequiredMixin, generic.CreateView):
    model = idea_models.Idea
    form_class = forms.IdeaForm
    permission_required = 'meinberlin_ideas.propose_idea'
    template_name = 'meinberlin_ideas/idea_create_form.html'

    def dispatch(self, *args, **kwargs):
        mod_slug = self.kwargs[self.slug_url_kwarg]
        self.module = Module.objects.get(slug=mod_slug)
        self.project = self.module.project
        return super().dispatch(*args, **kwargs)

    def get_permission_object(self, *args, **kwargs):
        return self.module

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.module.slug
        context['project'] = self.project
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.module = self.module
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['module'] = self.module
        return kwargs


class IdeaUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = idea_models.Idea
    form_class = forms.IdeaForm
    permission_required = 'meinberlin_ideas.modify_idea'
    template_name = 'meinberlin_ideas/idea_update_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['module'] = self.object.module
        return kwargs


class IdeaDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = idea_models.Idea
    success_message = _("Your Idea has been deleted")
    permission_required = 'meinberlin_ideas.modify_idea'
    template_name = 'meinberlin_ideas/idea_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(IdeaDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'project-detail', kwargs={'slug': self.object.project.slug})
