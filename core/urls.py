from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>/", views.by_category, name="by_category"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),

    # CRUD cho người đưa tin
    path("me/articles/", views.my_articles, name="my_articles"),
    path("me/articles/new/", views.article_create, name="article_create"),
    path("me/articles/<int:pk>/edit/", views.article_update, name="article_update"),
    path("me/articles/<int:pk>/delete/", views.article_delete, name="article_delete"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/approve/<int:pk>/", views.approve_article, name="approve_article"),
    path("admin-dashboard/reject/<int:pk>/", views.reject_article, name="reject_article"),
    path("admin-dashboard/users/", views.manage_users, name="manage_users"),
    path("admin-dashboard/articles/", views.manage_articles, name="manage_articles"),
    path("admin-dashboard/categories/delete/<int:pk>/", views.delete_category, name="delete_category"),
    path("admin-dashboard/categories/", views.manage_categories, name="manage_categories"),
]
