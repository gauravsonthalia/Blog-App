from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

def blogHome(request):
    allPost = Post.objects.all()
    context = {'allPost' : allPost}
    return render(request, 'blog/blogHome.html', context)

def blogpost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comment = BlogComment.objects.filter(post=post, parent=None) 
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    reply_dict = {}
    for reply in replies:
        if reply.parent.serial_number not in reply_dict.keys():
            reply_dict[reply.parent.serial_number] = [reply]
        else:
            reply_dict[reply.parent.serial_number].append(reply)
    context = {'post' : post, 'comment': comment, 'user': request.user, 'reply_dict': reply_dict}
    return render(request, 'blog/blogpost.html', context)

def postcomment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        post_sno = request.POST.get('post_sno') 
        post = Post.objects.get(serial_no = post_sno)
        parentSerial_number = request.POST.get('parentSerial_number')
        if parentSerial_number == '':
            comments = BlogComment(comment = comment, user=user, post=post)
        else:
            parent = BlogComment.objects.get(serial_number=parentSerial_number)
            comments = BlogComment(comment = comment, user=user, post=post, parent=parent)
        comments.save()
        messages.success(request, 'Hurray...')
    return redirect(f'/blog/{post.slug}')