from django import forms
from products.models import Product, Discussions, Comment


class ProdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'quantity', 'description', 'short_description', 'image', 'category')


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussions
        fields = ('name', 'description')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
