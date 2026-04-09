from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("add-entry/", views.add_entry, name="add_entry"),
    path('categories/', views.categories_view, name='categories'),
    path("categories/<int:category_id>/",  views.category_entries, name="category_entries"),
    path('entries/', views.view_entries, name='view_entries'),
    path('entries/edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('entries/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path("favourites/", views.favourite_entries, name="favourites"),
    path('remove-favourite/<int:entry_id>/', views.remove_from_favourites,name='remove_favourite'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]


