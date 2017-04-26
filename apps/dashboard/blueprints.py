from collections import namedtuple

from django.utils.translation import ugettext_lazy as _

from apps.budgeting import phases as budgeting_phases
from apps.documents import phases as documents_phases
from apps.extprojects import phases as extprojects_phases
from apps.ideas import phases as ideas_phases
from apps.mapideas import phases as mapideas_phases

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
         image='images/blueprints/brainstorming.svg',
         settings_model=None,
     )),
    ('map-brainstorming',
     ProjectBlueprint(
         title=_('Spatial Brainstorming'),
         description=_(
             'Collect location specific ideas for a topic and comment on them.'
         ),
         content=[
             mapideas_phases.CollectPhase(),
         ],
         image='images/blueprints/map-brainstorming.svg',
         settings_model=('a4maps', 'AreaSettings'),
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
         image='images/blueprints/agenda-setting.svg',
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
         image='images/blueprints/text-review.svg',
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
         image='images/blueprints/participatory-budgeting.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
    ('external-project',
     ProjectBlueprint(
         title=_('External project'),
         description=_(
             'External projects are handled on a different platform.'
         ),
         content=[
             extprojects_phases.ExternalPhase(),
         ],
         image='images/blueprints/external-project.svg',
         settings_model=None,
     )),
]


class BlueprintMixin():
    @property
    def blueprint(self):
        return dict(blueprints)[self.kwargs['blueprint_slug']]
