from urllib.parse import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm

# Create your views here.

def recent_posts(request):
    query_list = Post.objects.active()
    total_posts = query_list.count
    recent_articles = Post.objects.active()[:2]

    if request.user.is_staff or request.user.is_superuser:
        recent_articles = Post.objects.all()[:2]
        query_list = Post.objects.all()
        total_posts = query_list.count

    search_query = request.GET.get("q")
    if search_query:
        query_list = query_list.filter(
        Q(title__icontains=search_query) |
        Q(content__icontains=search_query) |
        Q(user__first_name__icontains=search_query) |
        Q(user__last_name__icontains=search_query)
        ).distinct()

        total_posts = query_list.count
        recent_articles = query_list

    context = {
    "page_title": "Recent Articles",
    "recent_articles": recent_articles,
    "all_articles": total_posts
    }

    return render(request,"index.html", context)


def post_list(request):
    query_list = Post.objects.active()
    total_posts = query_list.count
    # year_archive = year_archive2()
    if request.user.is_staff or request.user.is_superuser:
        query_list = Post.objects.all()

    search_query = request.GET.get("q")
    if search_query:
        query_list = query_list.filter(
        Q(title__icontains=search_query) |
        Q(content__icontains=search_query) |
        Q(user__first_name__icontains=search_query) |
        Q(user__last_name__icontains=search_query)
        ).distinct()

    paginator = Paginator(query_list, 5)
    page_request_var = "page"
    page = request.GET.get("page")

    total_posts = paginator.count
    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)

    context = {
    "list": page_list,
    "page_title": "All Articles",
    "page_request_var": page_request_var,
    "all_articles": total_posts
    }
    return render(request,"post_list.html", context)


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context= {
        "form": form,
        "page_title": "Create New Post"
    }
    return render(request,"post_create.html", context)

def post_detail(request, slug):
    instance = get_object_or_404(Post, slug= slug)

    share_string = quote_plus(instance.content)


    if instance.draft or instance.published_date > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    context = {
        "title": "instance.title",
        "instance": instance,
        "share_string": share_string,
    }

    return render(request,"post_detail.html", context)


def post_edit(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug= slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Post Was Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "page_title": "Edit Post"
    }
    return render(request,"post_create.html", context)


def post_delete(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id= id)
    instance.user = request.user
    instance.delete()
    messages.success(request, "Post Deleted Successfully")
    return redirect("post:list")


def year_archive(request, year):
    query_list = Post.objects.active().filter(published_date__year=year)
    context = {'year': year, 'article_list': query_list}
    return render(request, 'year_archive.html', context)

def month_archive(request, year, month):
    query_list = Post.objects.active().filter(published_date__month=month)
    context = {'month': month, 'article_list': query_list}
    return render(request, 'month.html', context)
