from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from . import view
from django.shortcuts import render, get_object_or_404
from .models import Post

urlpatterns = [
    path('', view.travelHome),
    path('travelhome',view.travelHome),
    path('404.html',view.error404),
    path('about.html',view.about),
    path('blog.html', view.blog, name='blog'),
    path('blog-single.html', view.blog_single, name='blog_single'),
    path('contact.html', view.contact),
    path('gallery.html', view.gallery),
    path('spot.html', view.spot_choose),
    path('route.html', view.route_show),
    path('reco', view.reco),
    path('route_design.html', view.route_design),
    path('api/gallery/', view.gallery, name='gallery'),
    path('login/', view.login_view, name='login'),
    path('logout/', view.logout_view, name='logout'),
    path('register/', view.register_view, name='register'),
    path('chat/', view.chat_view, name='chat'),
    path("seasonal/", view.seasonal_spot, name="seasonal_spot"),
    path('delete_comment/<int:comment_id>/', view.delete_comment, name='delete_comment'),
    path('post_create/', view.post_create, name='post_create'),
    path('delete_post/<int:post_id>/', view.delete_post, name='delete_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def blog_single(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog-single.html', {'post': post})


