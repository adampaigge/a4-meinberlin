from adhocracy4.categories import forms as category_forms
from adhocracy4.modules import forms as module_forms
from . import models


class ProposalForm(category_forms.CategorizableForm):

    class Meta:
        model = models.Proposal
        fields = ['name', 'description', 'category', 'budget']


class ProposalModerateForm(module_forms.ItemForm):

    def __init__(self, *args, **kwargs):
        super(ProposalModerateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Proposal
        fields = ['moderator_feedback']
