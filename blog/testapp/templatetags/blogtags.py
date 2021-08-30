from django import template
from testapp.models import Post
register=template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()
@register.inclusion_tag('testapp/latest_posts123.html')
def show_latest_posts(count=5):
  latest_posts=Post.objects.all().order_by('-publish')[:count]
  return {'latest_posts':latest_posts}

from django.db.models import Count
@register.simple_tag
def get_most_commented_posts(count=5):
 return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]