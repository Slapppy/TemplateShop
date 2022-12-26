from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Products
from store.forms import ProductCreate
from store.models.category import Category
from django.views import View


def upload_product(request):
    upload = ProductCreate()
    if request.method == 'POST':
        upload = ProductCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('homepage')
        else:
            return HttpResponse(
                """ Something went wrong." """)
    else:
        return render(request, 'Upload.html', {'upload_form': upload})

