from django import template

from .. import forms

register = template.Library()


@register.inclusion_tag('Cybersport/comment_form.html', takes_context=True)
def comment_form(context, object_type: str, obj):
    context['object_type'] = object_type
    context['obj'] = obj
    context['comment_form'] = forms.CommentForm()
    return context


@register.inclusion_tag('Cybersport/comments.html', takes_context=True)
def comments_block(context, obj):
    context['comments'] = obj.comments.order_by('-created_at')
    return context
