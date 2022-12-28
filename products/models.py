from django.db import models

from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='products_images', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=80, verbose_name='слаг', unique_for_date='created_at')
    user = models.ForeignKey(User, related_name='user', verbose_name='пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return f'Продукт: "{self.name}" категории: "{self.category}"'


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modificated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price


class Discussions(models.Model):
    user = models.ForeignKey(User, related_name='disc_user', verbose_name='пользователь', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=80, verbose_name='слаг', unique_for_date='created_at')
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)


class Comment(models.Model):
    discussions = models.ForeignKey(Discussions, verbose_name='форум', related_name='discussion_comments',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_comments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
