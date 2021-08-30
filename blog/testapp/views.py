from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from.models import Post,Comment
from.forms import Emailsendform,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

def post_list(request,tag_slug=None):
    post=Post.objects.all()
    tag=None
    if tag_slug:
       tag=get_object_or_404(Tag,slug=tag_slug)
       post=post.filter(tags__in=[tag])
    paginator=Paginator(post,2)
    page_number=request.GET.get('page')
    try:
       post=paginator.page(page_number)
    except PageNotAnInteger:
       post=paginator.page(1)
    except EmptyPage:
       post=paginator.page(paginator.num_pages)
    return render(request,'testapp/post_list.html',{'post':post,'tag':tag})

def post_detail(request,post):
    post1=get_object_or_404(Post,slug=post)
    comment=post1.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
     form=CommentForm(request.POST)
     if form.is_valid():
         new_comment=form.save(commit=False)
         new_comment.post=post1
         new_comment.save()
         csubmit=True
    else:
       form=CommentForm()
    return render(request,'testapp/post_detail.html',{'post1':post1,'form':form,'comment':comment,'csubmit':csubmit})

def sendbymail(request,id):
  post=Post.objects.get(id=id)
  form=Emailsendform()
  sent=False
  if request.method=='POST':
    form=Emailsendform(request.POST or None)
    if form.is_valid():
      cd=form.cleaned_data
      post_url=request.build_absolute_uri(post.get_absolute_url())
      subject='{} recommends you to read {}'.format(cd['name'],post.title)
      message=' Read post at {} \n comments {}'.format(post_url,cd['comments'])
      send_mail(subject,message,'ashumishra',[cd['to']])
      sent=True
  return render(request,'testapp/sendmail.html',{'post':post ,'form':form,'sent':sent})
