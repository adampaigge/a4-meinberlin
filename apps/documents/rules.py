import rules

from adhocracy4.modules import predicates as module_predicates


rules.add_perm(
    'meinberlin_documents.view',
    module_predicates.is_allowed_view_item
)


rules.add_perm(
    'meinberlin_documents.create',
    module_predicates.is_project_admin
)
