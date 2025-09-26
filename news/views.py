from django.shortcuts import render
from news import models as newsModels
from shop import models as shopModels



def home(request):
    category = shopModels.Category.objects.all()
    posts = newsModels.Post.objects.all()
    return render(request, 'news/home.html', {'posts':posts, 'category':category} )


def detail(request,id):
    category = shopModels.Category.objects.all()
    post = newsModels.Post.objects.get(pk=id)
    return render(request, 'news/detail.html',  {'post': post, 'category':category})



