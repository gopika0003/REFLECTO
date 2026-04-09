from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .models import Entry, Category
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count


def home(request):
    return render(request, "diary/home.html")


@login_required
def add_entry(request):
    categories = Category.objects.all()
    success = False

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")
        favourite = request.POST.get("favourite") == "on"
        
        category = None
        if category_id:
            category = get_object_or_404(Category, id=category_id)

        Entry.objects.create(
            user=request.user,
            title=title,
            content=content,
            category=category,
            is_favourite=favourite
        )

        messages.success(request, "✨ Entry saved successfully!")
        return redirect("add_entry")

        success = True
        if category:
            return redirect("category_entries", category_id=category.id)

        return redirect("add_entry")

    return render(request, "diary/entry.html", {
        "categories": categories
    })


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            # If admin → go to admin dashboard
            if user.is_staff or user.is_superuser:
                return redirect("admin_dashboard")

            # If normal user → go to user dashboard
            else:
                return redirect("dashboard")

        else:
            return HttpResponse("Invalid username or password.")

    return render(request, "diary/login.html")


# REGISTER
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not password1:
            messages.error(request, "All fields are required")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "diary/register.html")


@login_required
def categories_view(request):
    categories = Category.objects.all()

    return render(request, 'diary/categories.html', {
        'categories': categories
    })


@login_required
def category_entries(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    entries = Entry.objects.filter(
        category=category,
        user=request.user
    ).order_by('-created_at')

    return render(request, 'diary/category_entries.html', {
        'category': category,
        'entries': entries
    })


@login_required
def view_entries(request):
    entries = Entry.objects.filter(user=request.user).order_by('-created_at')

    search_date = request.GET.get('date')
    if search_date:
        entries = entries.filter(created_at__date=search_date)

    categories = Category.objects.all()

    return render(request, "diary/view.html", {
        "entries": entries,
        "categories": categories
    })


# EDIT ENTRY
@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)

    if request.method == "POST":
        entry.title = request.POST.get("title")
        entry.content = request.POST.get("content")

        category_id = request.POST.get("category")
        if category_id:
            entry.category = Category.objects.get(id=category_id)

        entry.is_favourite = request.POST.get("favourite") == "on"

        entry.save()
        messages.success(request, "Entry updated successfully!")

    return redirect("view_entries")


@login_required
def favourite_entries(request):
    entries = Entry.objects.filter(is_favourite=True, user=request.user).order_by('-created_at')

    return render(request, "diary/favourites.html", {
        "entries": entries
    })


@login_required
def remove_from_favourites(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    entry.is_favourite = False
    entry.save()
    return redirect('favourites')


# DELETE ENTRY
@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    entry.delete()
    messages.success(request, "Entry deleted successfully!")
    return redirect("view_entries")


# DASHBOARD
@login_required
def dashboard(request):
    return render(request, "diary/dashboard.html")


# -------------------------------
# ADMIN DASHBOARD 
# -------------------------------

@staff_member_required
def admin_dashboard(request):

    users = User.objects.filter(is_superuser=False).annotate(
        entry_count=Count('entry')
    ).order_by('-entry_count')

    total_users = User.objects.filter(is_superuser=False).count()

    context = {
        "users": users,
        "total_users": total_users
    }

    return render(request, "diary/admin_dashboard.html", context)