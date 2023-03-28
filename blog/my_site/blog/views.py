from django.shortcuts import render , get_object_or_404 , redirect
from .models import *
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def welcome(request):
    return render(request , 'blog/post/welcome.html')


def index(request):
    return render(request , 'blog/post/index.html')


def postlist(request):
    posts = Post.objects.all()
    return render(request , 'blog/post/list.html' , {"posts" : posts})


def postdetail(request , slug):
    post = get_object_or_404(Post, slug = slug)
    comments = post.comments.filter(active = True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit = False)       # Create Comment object but don't save to database yet
            new_comment.post = post     # Assign the current post to the comment
            new_comment.save()      # Save the comment to the database
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request , 'blog/post/detail.html' , context)



def UserAccount(request):
    user = request.user
    try:
        account = Account.objects.get(user = user)
    except:
        account = Account.objects.create(user = user)
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['name']
            user.last_name = form.cleaned_data['last_name']
            account.gender = form.cleaned_data['gender']
            account.address = form.cleaned_data['address']
            account.age = form.cleaned_data['age']
            account.phone = form.cleaned_data['phone']
            user.save()
            account.save()
            return redirect('blog:index') #if form was valid go to blog/index
        else:
            return render(request , 'blog/forms/account_form.html' , {'form' : form , 'account' : account})
    form = AccountForm()
    return render(request , 'blog/forms/account_form.html' , {'form' : form , 'account' : account})


def Signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username , password = password)
            login(request , user)
            return redirect('blog:index')
    else:
        form = UserCreationForm()
    return render(request , 'blog/forms/signup.html' , {'form' : form})