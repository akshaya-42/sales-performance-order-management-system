from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from app.models import Order, Product, Customer, Notification


@login_required
def dashboard_views(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Summary stats
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_amount'))['total'] or 0
    total_customers = Customer.objects.count()
    total_products = Product.objects.filter(is_active=True).count()

    # Monthly stats
    monthly_orders = Order.objects.filter(created_at__date__gte=month_start).count()
    monthly_revenue = Order.objects.filter(
        status='delivered', created_at__date__gte=month_start
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Recent orders
    recent_orders = Order.objects.select_related('customer', 'created_by').order_by('-created_at')[:5]

    # Low stock products
    low_stock = Product.objects.filter(stock__lt=10, is_active=True).order_by('stock')[:5]

    # Order status distribution
    order_status = Order.objects.values('status').annotate(count=Count('id'))

    # Last 7 days revenue (for sparkline)
    daily_revenue = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        rev = Order.objects.filter(
            status='delivered', created_at__date=day
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        daily_revenue.append({'day': day.strftime('%a'), 'revenue': float(rev)})

    # Notifications
    unread_notifications = request.user.notifications.filter(is_read=False).count()

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'total_products': total_products,
        'monthly_orders': monthly_orders,
        'monthly_revenue': monthly_revenue,
        'recent_orders': recent_orders,
        'low_stock': low_stock,
        'order_status': list(order_status),
        'daily_revenue': daily_revenue,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'dashboard.html', context)


@login_required
def notifications_views(request):
    notifications = request.user.notifications.all()
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications')


@login_required
def mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect('notifications')

@login_required
def dashboard_search(request):
    """Global search across orders, customers, and products."""
    from app.models import Product, Customer, Order
    from django.db.models import Q

    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', '')

    orders = []
    customers = []
    products = []

    if query:
        if search_type in ('', 'orders'):
            orders = Order.objects.filter(
                Q(order_number__icontains=query) |
                Q(customer__first_name__icontains=query) |
                Q(customer__last_name__icontains=query)
            ).select_related('customer')[:10]

        if search_type in ('', 'customers'):
            customers = Customer.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            )[:10]

        if search_type in ('', 'products'):
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(sku__icontains=query) |
                Q(description__icontains=query)
            ).filter(is_active=True)[:10]

    context = {
        'query': query,
        'search_type': search_type,
        'orders': orders,
        'customers': customers,
        'products': products,
        'total_results': len(list(orders)) + len(list(customers)) + len(list(products)),
    }
    return render(request, 'search_results.html', context)
