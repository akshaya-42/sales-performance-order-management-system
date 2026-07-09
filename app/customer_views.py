from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from app.models import Customer
from app.forms import CustomerForm
from app.decorators import staff_required


@login_required
def customer_list(request):
    customers = Customer.objects.all()

    # Search
    q = request.GET.get('q', '')
    if q:
        customers = customers.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(email__icontains=q) | Q(phone__icontains=q)
        )

    # Filter by city
    city = request.GET.get('city', '')
    if city:
        customers = customers.filter(city__icontains=city)

    # Sort
    sort = request.GET.get('sort', '-created_at')
    customers = customers.order_by(sort)

    # Pagination
    paginator = Paginator(customers, 10)
    page = request.GET.get('page')
    customers = paginator.get_page(page)

    return render(request, 'order_list.html', {
        'customers': customers, 'q': q, 'city': city,
    })


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    orders = customer.orders.order_by('-created_at')
    total_spent = customer.total_spent()
    return render(request, 'sales_app/customers/detail.html', {
        'customer': customer, 'orders': orders, 'total_spent': total_spent,
    })


@staff_required
def customer_create(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            messages.success(request, f"Customer '{customer.full_name}' created!")
            return redirect('customer_list')
    return render(request, 'customer_form.html', {'form': form, 'title': 'Add Customer'})


@staff_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated!")
            return redirect('customer_list')
    return render(request, 'customer_form.html', {'form': form, 'title': 'Edit Customer', 'customer': customer})


@staff_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, "Customer deleted.")
        return redirect('customer_list')
    return render(request, '/confirm_delete.html', {'object': customer, 'type': 'Customer'})