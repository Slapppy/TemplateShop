"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/', views.ForumListView.as_view(), name='forum'),
    path('forum/discussion/add/', login_required(views.DiscussionCreateView.as_view()), name='add_disc'),
    path('forum/discussion/<slug:slug>/<int:id>/', views.DiscDetailView.as_view(), name='detail_disc'),
    path('forum/discussion/<slug:slug>/<int:disc_id>/comment/<int:id>/delete', views.CommentDeleteView.as_view(),
         name='delete_comment'),
    path('forum/discussion/<slug:slug>/<int:disc_id>/comment/<int:id>/edit', views.CommentUpdateView.as_view(),
         name='update_comment'),
    path('products/', views.products, name='products'),
    path('<int:category_id>/products/', views.products, name='category'),
    path('page/<int:page>/', views.products, name='page'),
    path('baske_add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('basket_delete/<int:id>', views.basket_delete, name='basket_delete'),
    path('products/add/', views.ProductCreateView.as_view(), name='add_template'),
    path('<slug:slug>/<int:id>/delete', views.ProdDeleteView.as_view(), name='delete_template'),
    path('<slug:slug>/<int:id>/edit', views.ProdUpdateView.as_view(), name='update_template'),
]
