from __future__ import annotations

from django import template
from django.forms.renderers import get_default_renderer
from django.template.defaulttags import TemplateLiteral
from django.template.exceptions import TemplateSyntaxError


register = template.Library()


class ModalNode(template.Node):
    def __init__(self, nodelist, bits):
        self.nodelist = nodelist
        self.bits = bits

    def render(self, context):
        return get_default_renderer().render(
            "modal/basic.html",
            {
                "modal_id": self.bits.eval(context),
                "modal_content": self.nodelist.render(context),
            },
        )


@register.tag(name="modal")
def do_modal(parser, token):
    try:
        bits = token.split_contents()[1]
    except IndexError:
        raise TemplateSyntaxError('Malformed template tag at line {}: "{}"'.format(token.lineno, token.contents))
    nodelist = parser.parse(("endmodal",))
    parser.delete_first_token()
    return ModalNode(nodelist, TemplateLiteral(parser.compile_filter(bits), bits))
