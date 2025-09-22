from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group

from .models import Article, Category

PAGE_SIZE = 20


# Helper phân trang (keyset có thể làm nâng cao)
def paginate(queryset, page, size=PAGE_SIZE):
    offset = (page - 1) * size
    return queryset[offset:offset + size]


def home(request):
    q = (request.GET.get("q") or "").strip()
    page = int(request.GET.get("page", "1"))

    qs = Article.objects.filter(status="approved").order_by("-published_at", "-id")
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(short_desc__icontains=q) |
            Q(content__icontains=q)
        )

    articles = paginate(qs, page)
    return render(request, "core/home.html", {"articles": articles, "q": q, "page": page})



def by_category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    page = int(request.GET.get("page", "1"))
    qs = Article.objects.filter(category=cat).order_by("-published_at", "-id")
    articles = paginate(qs, page)
    return render(request, "core/by_category.html", {
        "category": cat,
        "articles": articles,
        "page": page
    })


def article_detail(request, pk):
    a = get_object_or_404(Article, pk=pk)

    if not request.user.is_staff and request.user != a.author and a.status != "approved":
        messages.error(request, "Bài viết này chưa được duyệt.")
        return redirect("home")

    return render(request, "core/article_detail.html", {"a": a})


@login_required
def my_articles(request):
    articles = Article.objects.filter(author=request.user).order_by("-published_at", "-id")[:200]
    return render(request, "core/my_articles.html", {"articles": articles})


@login_required
def article_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        short_desc = request.POST.get("short_desc", "").strip()
        content = request.POST.get("content", "").strip()
        category_id = request.POST.get("category_id")
        published_raw = request.POST.get("published_at")
        published_at = parse_datetime(published_raw) if published_raw else timezone.now()

        if not (title and short_desc and content and category_id):
            messages.error(request, "Thiếu dữ liệu bắt buộc.")
        else:
            Article.objects.create(
                title=title,
                short_desc=short_desc,
                content=content,
                category_id=category_id,
                author=request.user,
                published_at=published_at,
            )
            messages.success(request, "Đăng tin thành công.")
            return redirect("my_articles")

    categories = Category.objects.all().order_by("name")
    return render(request, "core/article_form.html", {"categories": categories})


@login_required
def article_update(request, pk):
    # Cho phép admin sửa mọi bài, user thường chỉ sửa bài của mình
    if request.user.is_superuser:
        a = get_object_or_404(Article, pk=pk)
    else:
        a = get_object_or_404(Article, pk=pk, author=request.user)

    if request.method == "POST":
        a.title = request.POST.get("title") or a.title
        a.short_desc = request.POST.get("short_desc") or a.short_desc
        a.content = request.POST.get("content") or a.content
        a.category_id = request.POST.get("category_id") or a.category_id

        published_raw = request.POST.get("published_at")
        if published_raw:
            parsed = parse_datetime(published_raw)
            if parsed:
                a.published_at = parsed

        a.save()
        messages.success(request, "Cập nhật thành công.")
        return redirect("my_articles")

    categories = Category.objects.all().order_by("name")
    return render(request, "core/article_form.html", {"a": a, "categories": categories})


@login_required
def article_delete(request, pk):
    # Cho phép admin xoá mọi bài, user thường chỉ xoá bài của mình
    if request.user.is_superuser:
        a = get_object_or_404(Article, pk=pk)
    else:
        a = get_object_or_404(Article, pk=pk, author=request.user)

    if request.method == "POST":
        a.delete()
        messages.success(request, "Đã xoá bài viết.")
        return redirect("my_articles")

    return render(request, "core/article_confirm_delete.html", {"a": a})



@staff_member_required
def admin_dashboard(request):
    stats = {
        "total_articles": Article.objects.count(),
        "total_users": User.objects.count(),
        "total_categories": Category.objects.count(),
    }
    recent = Article.objects.order_by("-published_at")[:5]
    pending = Article.objects.filter(status="pending").order_by("-published_at")

    return render(request, "core/admin_dashboard.html", {
        "stats": stats,
        "recent": recent,
        "pending": pending,
    })

@staff_member_required
def approve_article(request, pk):
    a = get_object_or_404(Article, pk=pk)
    a.status = "approved"
    a.save()
    messages.success(request, f"Đã duyệt bài: {a.title}")
    return redirect("admin_dashboard")

@staff_member_required
def reject_article(request, pk):
    a = get_object_or_404(Article, pk=pk)
    a.status = "rejected"
    a.save()
    messages.error(request, f"Đã từ chối bài: {a.title}")
    return redirect("admin_dashboard")

@staff_member_required
def manage_users(request):
    users = User.objects.all().order_by("username")
    groups = Group.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        group_id = request.POST.get("group_id")
        user = get_object_or_404(User, pk=user_id)
        group = get_object_or_404(Group, pk=group_id)

        # clear nhóm cũ, gán nhóm mới
        user.groups.clear()
        user.groups.add(group)

        messages.success(request, f"Đã gán quyền {group.name} cho {user.username}")
        return redirect("manage_users")

    return render(request, "core/manage_users.html", {"users": users, "groups": groups})

@staff_member_required
def manage_articles(request):
    category_id = request.GET.get("category")
    articles = Article.objects.all().order_by("-published_at")

    if category_id:
        articles = articles.filter(category_id=category_id)

    categories = Category.objects.all().order_by("name")
    return render(request, "core/manage_articles.html", {
        "articles": articles,
        "categories": categories,
        "selected_category": category_id,
    })

@staff_member_required
def manage_categories(request):
    categories = Category.objects.all().order_by("name")

    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            slug = name.lower().replace(" ", "-")
            Category.objects.create(name=name, slug=slug)
            messages.success(request, f"Đã tạo danh mục: {name}")
            return redirect("manage_categories")

    return render(request, "core/manage_categories.html", {"categories": categories})

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, f"Đã xóa danh mục '{category.name}'")
    return redirect("manage_categories")