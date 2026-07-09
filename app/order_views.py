from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from app.models import Order, OrderItem, Notification
from app.forms import OrderForm, OrderItemFormSet
from app.decorators import staff_required


@login_required
def order_list(request):
    orders = Order.objects.select_related('customer', 'created_by')

    # Search
    q = request.GET.get('q', '')
    if q:
        orders = orders.filter(
            Q(order_number__icontains=q) |
            Q(customer__first_name__icontains=q) |
            Q(customer__last_name__icontains=q)
        )

    # Filter
    status = request.GET.get('status', '')
    payment = request.GET.get('payment', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if status:
        orders = orders.filter(status=status)
    if payment:
        orders = orders.filter(payment_method=payment)
    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)

    # Sort
    sort = request.GET.get('sort', '-created_at')
    orders = orders.order_by(sort)

    # Pagination
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    orders = paginator.get_page(page)

    return render(request, 'order_list.html', {
        'orders': orders, 'q': q,
        'selected_status': status,
        'selected_payment': payment,
        'date_from': date_from, 'date_to': date_to,
        'status_choices': Order.STATUS_CHOICES,
        'payment_choices': Order.PAYMENT_CHOICES,
    })


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('customer', 'created_by'), pk=pk)
    items = order.items.select_related('product')
    return render(request, 'order_detail.html', {'order': order, 'items': items})


@staff_required
def order_create(request):
    form = OrderForm()
    formset = OrderItemFormSet()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            formset.instance = order
            formset.save()
            order.calculate_total()
            # Create notification
            Notification.objects.create(
                user=request.user,
                title="New Order Created",
                message=f"Order {order.order_number} has been created for {order.customer.full_name}.",
                notification_type='success'
            )
            messages.success(request, f"Order {order.order_number} created!")
            return redirect('order_detail', pk=order.pk)
    return render(request, 'order_form.html', {
        'form': form, 'formset': formset, 'title': 'Create Order',
    })


@staff_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(instance=order)
    formset = OrderItemFormSet(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            order.calculate_total()
            messages.success(request, f"Order {order.order_number} updated!")
            return redirect('order_detail', pk=order.pk)
    return render(request, 'order_form.html', {
        'form': form, 'formset': formset, 'title': 'Edit Order', 'order': order,
    })


@staff_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order deleted.")
        return redirect('order_list')
    return render(request, 'confirm_delete.html', {'object': order, 'type': 'Order'})


@staff_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            if new_status == 'delivered':
                order.delivered_at = timezone.now()
            order.save()
            Notification.objects.create(
                user=request.user,
                title="Order Status Updated",
                message=f"Order {order.order_number} status changed to {new_status}.",
                notification_type='info'
            )
            messages.success(request, f"Order status updated to {new_status}.")
    return redirect('order_detail', pk=pk)

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.db.models import Q
# from django.utils import timezone
# from app.models import Order, OrderItem, Notification
# from app.forms import OrderForm, OrderItemFormSet
# from app.decorators import staff_required


# @login_required
# def order_list(request):
#     orders = Order.objects.select_related('customer', 'created_by')

#     # Search
#     q = request.GET.get('q', '')
#     if q:
#         orders = orders.filter(
#             Q(order_number__icontains=q) |
#             Q(customer__first_name__icontains=q) |
#             Q(customer__last_name__icontains=q)
#         )

#     # Filter
#     status = request.GET.get('status', '')
#     payment = request.GET.get('payment', '')
#     date_from = request.GET.get('date_from', '')
#     date_to = request.GET.get('date_to', '')

#     if status:
#         orders = orders.filter(status=status)
#     if payment:
#         orders = orders.filter(payment_method=payment)
#     if date_from:
#         orders = orders.filter(created_at__date__gte=date_from)
#     if date_to:
#         orders = orders.filter(created_at__date__lte=date_to)

#     # Sort
#     sort = request.GET.get('sort', '-created_at')
#     orders = orders.order_by(sort)

#     # Pagination
#     paginator = Paginator(orders, 10)
#     page = request.GET.get('page')
#     orders = paginator.get_page(page)

#     return render(request, 'order_list.html', {
#         'orders': orders, 'q': q,
#         'selected_status': status,
#         'selected_payment': payment,
#         'date_from': date_from, 'date_to': date_to,
#         'status_choices': Order.STATUS_CHOICES,
#         'payment_choices': Order.PAYMENT_CHOICES,
#     })


# @login_required
# def order_detail(request, pk):
#     order = get_object_or_404(Order.objects.select_related('customer', 'created_by'), pk=pk)
#     items = order.items.select_related('product')
#     return render(request, 'app/detail.html', {'order': order, 'items': items})


# @staff_required
# def order_create(request):
#     form = OrderForm()
#     formset = OrderItemFormSet()
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         formset = OrderItemFormSet(request.POST)
#         if form.is_valid() and formset.is_valid():
#             order = form.save(commit=False)
#             order.created_by = request.user
#             order.save()
#             formset.instance = order
#             formset.save()
#             order.calculate_total()
#             # Create notification
#             Notification.objects.create(
#                 user=request.user,
#                 title="New Order Created",
#                 message=f"Order {order.order_number} has been created for {order.customer.full_name}.",
#                 notification_type='success'
#             )
#             messages.success(request, f"Order {order.order_number} created!")
#             return redirect('order_detail', pk=order.pk)
#     return render(request, 'form.html', {
#         'form': form, 'formset': formset, 'title': 'Create Order',
#     })


# @staff_required
# def order_edit(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     form = OrderForm(instance=order)
#     formset = OrderItemFormSet(instance=order)
#     if request.method == 'POST':
#         form = OrderForm(request.POST, instance=order)
#         formset = OrderItemFormSet(request.POST, instance=order)
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             order.calculate_total()
#             messages.success(request, f"Order {order.order_number} updated!")
#             return redirect('order_detail', pk=order.pk)
#     return render(request, 'form.html', {
#         'form': form, 'formset': formset, 'title': 'Edit Order', 'order': order,
#     })


# @staff_required
# def order_delete(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     if request.method == 'POST':
#         order.delete()
#         messages.success(request, "Order deleted.")
#         return redirect('order_list')
#     return render(request, '/confirm_delete.html', {'object': order, 'type': 'Order'})


# @staff_required
# def update_order_status(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     if request.method == 'POST':
#         new_status = request.POST.get('status')
#         if new_status in dict(Order.STATUS_CHOICES):
#             order.status = new_status
#             if new_status == 'delivered':
#                 order.delivered_at = timezone.now()
#             order.save()
#             Notification.objects.create(
#                 user=request.user,
#                 title="Order Status Updated",
#                 message=f"Order {order.order_number} status changed to {new_status}.",
#                 notification_type='info'
#             )
#             messages.success(request, f"Order status updated to {new_status}.")
#     return redirect('order_detail', pk=pk)