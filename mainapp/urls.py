from django.urls import path
from.import views

urlpatterns = [
    path("", views.Index, name = "Index"),
    path("about/", views.About, name = "About"),
    path("blog/", views.Blog, name = "Blog"),
    path("blog-details/<slug:slug>", views.BlogDetails, name = "BlogDetails"),
    path("contact/", views.Contact, name = "Contact"),
]
