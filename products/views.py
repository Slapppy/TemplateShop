from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView
from .models import Product, ProductCategory, Basket, Discussions, Comment
from django.views.generic.edit import FormMixin
from django.utils.text import slugify
from .forms import ProdForm, DiscussionForm, CommentForm
from django.urls import reverse


def index(request):
    return render(request, 'products/index.html', {
        'title': 'Store'
    })


def products(request, category_id=None, page=1):
    context = {
        'title': 'Store - products',
        'categories': ProductCategory.objects.all(),
    }
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 3)
    products_paginator = paginator.page(page)
    context.update({'products': products_paginator})
    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(current_page)


@login_required
def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProductCreateView(CreateView):
    template_name = 'products/create_prod.html'
    form_class = ProdForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('products')


class ProdDeleteView(DeleteView):
    template_name = 'products/delete_product.html'
    model = Product
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('products')


class ProdUpdateView(UpdateView):
    template_name = 'products/prod_edit.html'
    model = Product
    form_class = ProdForm
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('products')

    def get_context_data(self, **kwargs):
        print(self.kwargs)
        return {
            **super(ProdUpdateView, self).get_context_data(**kwargs),
            'slug': self.kwargs['slug'],
            'id': self.kwargs['id']
        }


class ForumListView(ListView):
    model = Discussions
    template_name = 'products/forum.html'
    context_object_name = 'discussions'


class DiscussionCreateView(CreateView):
    template_name = 'products/create_discussion.html'
    form_class = DiscussionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('forum')


class DiscDetailView(FormMixin, DetailView):
    template_name = 'products/one_disc.html'
    form_class = CommentForm
    model = Discussions
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.discussions = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_disc', args=(self.kwargs['slug'], self.kwargs['id']))


class CommentUpdateView(UpdateView):
    template_name = 'products/comment_edit.html'
    model = Comment
    form_class = CommentForm
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.text, allow_unicode=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_disc', args=(self.kwargs['slug'], self.kwargs['disc_id']))

    def get_context_data(self, **kwargs):
        return {
            **super(CommentUpdateView, self).get_context_data(**kwargs),
            'slug': self.kwargs['slug'],
            'disc_id': self.kwargs['id']
        }


class CommentDeleteView(DeleteView):
    model = Comment
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('detail_disc', args=(self.kwargs['slug'], self.kwargs['disc_id']))
