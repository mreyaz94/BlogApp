from django.shortcuts import render,get_object_or_404
from blog.models import Post,Comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag # Tag import from model.py of taggit application

# Create your views here.

def post_list_view(request,tag_slug=None):
    post_list = Post.objects.filter(status='published') # application level filter
    #----------------------------------------------------
    tag=None             #Tag operation
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug) # Tag is model_name inside taggit application
        post_list=post_list.filter(tags__in=[tag])
    #----------------------------------------------------
    # predefine class:-page,Paginator, num_pages
    p = Paginator(post_list,2)          # Paginator class define per page how many data contain from QuerySet. here 2 object contain per page
    page_num = request.GET.get('page')  # page_num is user-define-variable can be anything and page is predefine
    try:                                # If page is with in range(http://127.0.0.1:8000/list/?page=3), deliver 3rd page of results
        post_list = p.page(page_num)
    except PageNotAnInteger:     # If page is not an integer in url-http://127.0.0.1:8000/list/, deliver first page.
        post_list = p.page(1)  # display First page like "Page 1 of 4"
    except EmptyPage:               # If page is out of range (http://127.0.0.1:8000/list/?page=9999), deliver last page of results.
        post_list = p.page(p.num_pages)      # p.num_pages contain total number of page
    #-----------------------------------------------------
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag})

def post_detail_view(request,year,month,day,post):
    post = get_object_or_404(Post,slug = post,
                           status ='published',
                           publish__year = year,
                           publish__month = month,
                           publish__day = day)
            #------------------------------------------------
    comments = post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
            #------------------------------------------------
    return render(request,'blog/post_detail.html',{'post':post, 'form':form, 'csubmit':csubmit, 'comments':comments})

from django.core.mail import send_mail
from blog.forms import EmailSendForm,CommentForm

def mail_send_view(request,id):
    post = get_object_or_404(Post,id = id, status = 'published')
    sent = False
    if request.method  == 'POST':
            form = EmailSendForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                subject = '{}({}) recommends you to read"{}"'.format(cd['name'],cd['email'],post.title)
                post_url = request.build_absolute_uri(post.get_absolute_url())
                message = "Read Post At:\n {}\n\n{}\'s Comment:\n{}".format(post_url,cd['name'],cd['comments'])
                send_mail(subject,message,'shalapagal@blog.com',[cd['to']])
                sent =True
    else:
        form = EmailSendForm()
    return render(request,'blog/sharebyemail.html', {'form': form,'post': post, 'sent':sent})
