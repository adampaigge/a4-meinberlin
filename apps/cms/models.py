from django.db import models
from django.forms import widgets
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailadmin import edit_handlers
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore import fields
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from adhocracy4.projects.models import Project


class ProjectSelectionBlock(blocks.ChooserBlock):
    target_model = Project
    widget = widgets.Select

    def value_for_form(self, value):
        if isinstance(value, Project):
            return value.pk
        return value


class ProjectsWrapperBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=80)
    projects = blocks.ListBlock(
        ProjectSelectionBlock(label='Project'),
    )

    class Meta:
        template = 'meinberlin_cms/blocks/projects_block.html'


class CallToActionBlock(blocks.StructBlock):
    body = blocks.RichTextBlock()
    link = blocks.CharBlock()
    link_text = blocks.CharBlock(max_length=50, label='Link Text')

    class Meta:
        template = 'meinberlin_cms/blocks/cta_block.html'


class ColumnsBlock(blocks.StructBlock):
    columns_count = blocks.ChoiceBlock(choices=[
        (2, 'Two columns'),
        (3, 'Three columns'),
        (4, 'Four columns'),
    ], default=2)

    columns = blocks.ListBlock(
        blocks.RichTextBlock(label='Column body'),
    )

    class Meta:
        template = 'meinberlin_cms/blocks/columns_block.html'


class HomePage(Page):
    body = fields.StreamField([
        ('paragraph', blocks.RichTextBlock(
            template='meinberlin_cms/blocks/richtext_block.html'
        )),
        ('call_to_action', CallToActionBlock()),
        ('columns_text', ColumnsBlock()),
        ('projects', ProjectsWrapperBlock()),
    ])

    subtitle = models.CharField(max_length=120)

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        edit_handlers.FieldPanel('subtitle'),
        ImageChooserPanel('header_image'),
        edit_handlers.StreamFieldPanel('body'),
    ]


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    link_page = models.ForeignKey('wagtailcore.Page')

    @property
    def url(self):
        return self.link_page.url

    def __str__(self):
        return self.title

    panels = [
        edit_handlers.FieldPanel('title'),
        edit_handlers.PageChooserPanel('link_page')
    ]


@register_snippet
class NavigationMenu(ClusterableModel):
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title

    panels = [
        edit_handlers.FieldPanel('title'),
        edit_handlers.InlinePanel('items')
    ]


class NavigationMenuItem(Orderable, MenuItem):
    parent = ParentalKey('meinberlin_cms.NavigationMenu', related_name='items')
