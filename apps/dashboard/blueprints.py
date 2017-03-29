from collections import namedtuple

from django.utils.translation import ugettext_lazy as _

from apps.budgeting import phases as budgeting_phases
from apps.documents import phases as documents_phases
from apps.ideas import phases as ideas_phases

ProjectBlueprint = namedtuple(
    'ProjectBlueprint', [
        'title', 'description', 'content', 'image', 'settings_model'
    ]
)

blueprints = [
    ('brainstorming',
     ProjectBlueprint(
         title=_('Brainstorming'),
         description=_(
             'Collect first ideas for a specific topic and comment on them.'
         ),
         content=[
             ideas_phases.CollectPhase(),
         ],
         image='images/LOGO.png',
         settings_model=None,
     )),
    ('agenda-setting',
     ProjectBlueprint(
         title=_('Agenda Setting'),
         description=_(
             'With Agenda-Setting it’s possible to identify topics and to '
             'define mission statements. Afterwards anyone can comment and '
             'rate on different topics.'
         ),
         content=[
             ideas_phases.CollectPhase(),
             ideas_phases.RatingPhase(),
         ],
         image='images/LOGO.png',
         settings_model=None,
     )),
    ('text-review',
     ProjectBlueprint(
         title=_('Text Review'),
         description=_(
             'In the text-review it’s possible to structure draft texts '
             'co-operativly and rate and comment on them.'
         ),
         content=[
             documents_phases.CreateDocumentPhase(),
             documents_phases.CommentPhase(),
         ],
         image='images/LOGO.png',
         settings_model=None,
     )),
    ('participatory-budgeting',
     ProjectBlueprint(
         title=_('Participatory budgeting'),
         description=_(
             'With participatory-budgeting it’s possible to make proposals '
             'with budget specifications and locate them. Afterwards anyone '
             'can comment and rate on different proposals.'
         ),
         content=[
             budgeting_phases.RequestPhase(),
             budgeting_phases.FeedbackPhase(),
         ],
         image='images/LOGO.png',
         settings_model=None,
     )),
]


class BlueprintMixin():
    @property
    def blueprint(self):
        return dict(blueprints)[self.kwargs['blueprint_slug']]
