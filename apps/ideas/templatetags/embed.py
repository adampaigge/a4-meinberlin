from django import template

register = template.Library()


class EmbedURLNode(template.defaulttags.URLNode):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self, context):
        asvar = self._wrapped.asvar
        self._wrapped.asvar = False
        url = self._wrapped.render(context)
        self._wrapped.asvar = asvar

        request = context['request']
        if 'embed' in request.GET:
            url += '?embed'

        if asvar:
            context[asvar] = url
            return ''
        else:
            return url


@register.tag
def embed_url(parser, token):
    node = template.defaulttags.url(parser, token)
    return EmbedURLNode(node)
