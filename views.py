from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm, LoginForm, BlogForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Blog
from django.contrib.auth.models import Group
from django.shortcuts import redirect

from django.views import View

from django.views.generic import ListView, DetailView

from .models import Article


# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    return render(request,'blog/home.html',{'blogs':blogs})

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"CONGRATULATION, You are Registered!")
            user = form.save()
            group = Group.objects.get(name = 'Author')
            user.groups.add(group)
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request = request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                pwd = form.cleaned_data['password']
                user = authenticate(username=uname, password=pwd)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html',{'blogs':blogs,'full_name':full_name,'groups':gps})

def add_blog(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlogForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                cont = form.cleaned_data['cont']
                blg = Blog(title=title, cont = cont)
                blg.save()
                form = BlogForm()
        else:
            form = BlogForm()
        return render(request, 'blog/addblog.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def update_blog(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Blog.objects.get(pk=id)
            form = BlogForm(request.POST,instance = pi)
            if form.is_valid():
                form.save()
        else:
            pi = Blog.objects.get(pk=id)
            form = BlogForm(instance=pi)
        return render(request, 'blog/updateblog.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_blog(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Blog.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')



class Index(ListView): 
    model = Blog

    queryset = Blog.objects.all().order_by('-date')

    template_name = 'blog/index.html'

    paginate_by = 1

class DetailArticleView(DetailView):

    model = Blog

    template_name = 'blog/addblog.html'

    def get_context_data(self, *args, **kwargs):

        context = super(DetailArticleView, self).get_context_data(*args, **kwargs)

        context['liked_by_user'] = False 

        article = Blog.objects.get(id=self.kwargs.get('pk'))
        if article.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
        return context
    
class LikeArticle(View):

    def post(self, request, pk):

        article = Blog.objects.get(id=pk)

        if article.likes.filter(pk=self.request.user.id).exists():
            article.likes.remove(request.user.id)

        else:

            article.likes.add(request.user.id)

        article.save()

        return redirect('detail_article', pk)    