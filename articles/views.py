from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Article
from django.contrib.auth.decorators import login_required
from .forms import CreateArticle, CommentForm
def article_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request, "articles/article_list.html", {"articles": articles})

def article_detail(request, slug):
    template_name = 'articles/article_detail.html'
    post = get_object_or_404(Article, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'article': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

@login_required(login_url="/accounts/login/")
def article_create(request):
    if request.method == "POST":
        form = CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("articles:list")
    else:
        form = CreateArticle()
    return render(request, "articles/article_create.html", {"form":form})

