from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse
from apps.blog.models import BlogCategory, Article, Tag, Comments
from apps.blog.forms import CommentForm

def blog_category_list(request):
    blog_categories =BlogCategory.objects.all()
    breadcrumbs = {'current': 'Блог'}
    return render(request, 'blog/category_list.html', {"categories": blog_categories, "breadcrumbs": breadcrumbs})

def article_list(request, category_id):
    articles = Article.objects.filter(category_id=category_id)
    category = BlogCategory.objects.get(id=category_id)
    breadcrumbs = {
        reverse('blog_category_list'): 'Блог',
        'current': category.name
    }
    return render(
        request,
        'blog/article_list.html',
        {"articles": articles, "category": category, "breadcrumbs": breadcrumbs}
    )


@login_required
def article_view(request, category_id, article_id):
    category = BlogCategory.objects.get(id=category_id)
    article = Article.objects.get(id=article_id)
    breadcrumbs = {
        reverse('blog_category_list'): 'Блог',
        reverse('blog_article_list', args=[category_id]): category.name,
        'current': article.title
    }

    error = None
    user = request.user
    if request.method == 'POST':
        data = request.POST.copy()
        data.update(article=article)
        if user.is_authenticated:
            data.update(user=user, username=user.username, email=user.email, is_checked=True)
        else:
            data.update(is_active=False)
        request.POST = data
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    comment = form.save()
                    breadcrumbs = {'current': 'Комментарий сохранён'}
                    return render(
                        request, 'blog/created_comment.html',
                        {'article': article, 'breadcrumbs': breadcrumbs, 'comment': comment,
                         'article_id': article.id,
                         'category_id':article.category.id }
                    )
            except Exception as e:
                error = f'Комментарий не сохранился. {e}. Попробуйте ещё раз.'
        else:
            error = form.errors
    else:
        if user.is_authenticated:
            form = CommentForm(data={
                'username': user.username,
                'email': user.email
            })
        else:
            form = CommentForm()
    comments = Comments.objects.filter(article=article, is_checked=True, is_active=True)
    return render(
        request,
        'blog/article_view.html',
        {"category": category, "article": article, "form": form, "comments": comments,
         "breadcrumbs": breadcrumbs, "error": error}
    )

def tag_view(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    articles = Article.objects.filter(tags=tag)
    breadcrumbs = {
        reverse('blog_category_list'): 'Блог',
        'current': tag.name
    }
    return render(
        request,
        'blog/tag_view.html',
        {"tag": tag, "articles": articles, "breadcrumbs": breadcrumbs})

