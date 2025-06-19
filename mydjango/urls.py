from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

from django.urls import path, include
from . import view

urlpatterns = [
    path('', view.travelHome),
    path('travelhome',view.travelHome),
    path('404.html',view.error404),
    path('about.html',view.about),
    path('blog.html', view.blog),
    path('blog-single.html', view.blog_single),
    path('contact.html', view.contact),
    path('gallery.html', view.gallery),
    path('route_design.html', view.route_design),
    path('login/', view.login_view, name='login'),
    path('logout/', view.logout_view, name='logout'),
    path('register/', view.register_view, name='register'),
    path('chat/', view.chat_view, name='chat'),
    path("seasonal/", view.seasonal_spot, name="seasonal_spot"),
]


