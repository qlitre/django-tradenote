from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータの一部を置き換える。"""
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()


# 追加
@register.filter
def markdown_to_html(text):
    """マークダウンをhtmlに変換する。"""
    html = markdown.markdown(text, extensions=settings.MARKDOWN_EXTENSIONS)
    return mark_safe(html)
