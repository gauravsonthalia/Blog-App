from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['tel']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:   
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Thank you for contacting with us. We will get back to you soon.")
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPost = []
    else:
        allPostTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(content__icontains=query)
        allPost = allPostTitle.union(allPostContent)
    context = {'allPost' : allPost, 'query' : query}

    return render(request, 'home/search.html', context)

def handlesignup(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        username = request.POST['username']
        # Check for errorenous inputs
        if len(username) > 10:
            messages.error(request, 'Username must be less than 10 digit')
            return redirect('home')

        if not username.isalnum():
            messages.error(request, 'Username should only contains number and letters')
            return redirect('home')
        
        if password != confirm_password:
            messages.error(request, 'Password and Confirm Password did not match')
            return redirect('home')


            # Create the user
        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = first_name
        my_user.last_name = last_name
        my_user.save()
        messages.success(request, 'Your thoughts account has been created')
        return redirect('/')

    else:
        return HttpResponse('404 - Not Found')

def handlelogin(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        login_password = request.POST['login_password']
        
        user = authenticate(username = user_name, password=login_password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect ('home')

    return HttpResponse('404 - Not Found')


def handlelogout(request):
    logout(request)
    messages.success(request, 'You are Successfully Logged Out.')
    return redirect('home')
    