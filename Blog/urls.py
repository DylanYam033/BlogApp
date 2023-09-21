from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', PostListView.as_view(), name='list_post'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('detail/<slug>/', PostDetailView.as_view(), name='detail_post'),
    path('update/<slug>/', PostUpdateView.as_view(), name='update_post'),
    path('delete/<slug>/', PostDeleteView.as_view(), name='delete_post'),
    path('like/<slug>/', like, name='like_post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

