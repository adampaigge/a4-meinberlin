from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.modules.models import Module
from adhocracy4.projects import mixins

from . import models as idea_models
from . import forms


class IdeaListView(mixins.ProjectMixin, generic.ListView):
    model = idea_models.Idea


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


class IdeaUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = idea_models.Idea
    form_class = forms.IdeaForm
    permission_required = 'meinberlin_ideas.update_idea'
    template_name = 'meinberlin_ideas/idea_update_form.html'
