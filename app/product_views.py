from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from app.models import Product, Category
from app.forms import ProductForm, CategoryForm
from app.decorators import staff_required


@login_required
def product_list(request):
    products = Product.objects.select_related('category').prefetch_related('tags')

    # Search
    q = request.GET.get('q', '')
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(sku__icontains=q) | Q(description__icontains=q)
        )

    # Filter
    category_id = request.GET.get('category', '')
    status = request.GET.get('status', '')
    if category_id:
        products = products.filter(category_id=category_id)
    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)
    elif status == 'low_stock':
        products = products.filter(stock__lt=10)

    # Sort
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)

    # Pagination
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    categories = Category.objects.all()
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'q': q,
        'selected_category': category_id,
        'selected_status': status,
    })


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


@staff_required
def product_create(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' created successfully!")
            return redirect('product_list')
    return render(request, 'product_form.html', {'form': form, 'title': 'Add Product'})


@staff_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated!")
            return redirect('product_list')
    return render(request, 'product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})


@staff_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect('product_list')
    return render(request, 'confirm_delete.html', {'object': product, 'type': 'Product'})


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


@staff_required
def category_create(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created!")
            return redirect('app:category_list')
    return render(request, 'category_form.html', {'form': form, 'title': 'Add Category'})


@staff_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated!")
            return redirect('app:category_list')
    return render(request, 'category_form.html', {'form': form, 'title': 'Edit Category'})


@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted.")
        return redirect('app:category_list')
    return render(request, 'confirm_delete.html', {'object': category, 'type': 'Category'})

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.db.models import Q
# from app.models import Product, Category
# from app.forms import ProductForm, CategoryForm
# from app.decorators import staff_required


# @login_required
# def product_list(request):
#     products = Product.objects.select_related('category').prefetch_related('tags')

#     # Search
#     q = request.GET.get('q', '')
#     if q:
#         products = products.filter(
#             Q(name__icontains=q) | Q(sku__icontains=q) | Q(description__icontains=q)
#         )

#     # Filter
#     category_id = request.GET.get('category', '')
#     status = request.GET.get('status', '')
#     if category_id:
#         products = products.filter(category_id=category_id)
#     if status == 'active':
#         products = products.filter(is_active=True)
#     elif status == 'inactive':
#         products = products.filter(is_active=False)
#     elif status == 'low_stock':
#         products = products.filter(stock__lt=10)

#     # Sort
#     sort = request.GET.get('sort', '-created_at')
#     products = products.order_by(sort)

#     # Pagination
#     paginator = Paginator(products, 10)
#     page = request.GET.get('page')
#     products = paginator.get_page(page)

#     categories = Category.objects.all()
#     return render(request, 'product_list.html', {
#         'products': products,
#         'categories': categories,
#         'q': q,
#         'selected_category': category_id,
#         'selected_status': status,
#     })


# @login_required
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'customer_detail.html', {'product': product})


# @staff_required
# def product_create(request):
#     form = ProductForm()
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save()
#             messages.success(request, f"Product '{product.name}' created successfully!")
#             return redirect('product_list')
#     return render(request, 'product_form.html', {'form': form, 'title': 'Add Product'})


# @staff_required
# def product_edit(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     form = ProductForm(instance=product)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Product '{product.name}' updated!")
#             return redirect('product_list')
#     return render(request, 'product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})


# @staff_required
# def product_delete(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         product.delete()
#         messages.success(request, "Product deleted.")
#         return redirect('product_list')
#     return render(request, 'confirm_delete.html', {'object': product, 'type': 'Product'})


# @login_required
# def category_list(request):
#     categories = Category.objects.all()
#     return render(request, 'categories.html', {'categories': categories})


# @staff_required
# def category_create(request):
#     form = CategoryForm()
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Category created!")
#             return redirect('app:category_list')
#     return render(request, 'category_form.html', {'form': form, 'title': 'Add Category'})


# @staff_required
# def category_edit(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     form = CategoryForm(instance=category)
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, instance=category)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Category updated!")
#             return redirect('app:category_list')
#     return render(request, 'category_form.html', {'form': form, 'title': 'Edit Category'})


# @staff_required
# def category_delete(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     if request.method == 'POST':
#         category.delete()
#         messages.success(request, "Category deleted.")
#         return redirect('app:category_list')
#     return render(request, 'confirm_delete.html', {'object': category, 'type': 'Category'})