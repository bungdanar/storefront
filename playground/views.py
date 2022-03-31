from django.shortcuts import render
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models import Value, F, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from store.models import Collection, Customer, Product, OrderItem, Order
from tags.models import TaggedItem


def say_hello(request):
    # queryset = Customer.objects.annotate(
    #     full_name=Func(F('first_name'), Value(
    #         ' '), F('last_name'), function='CONCAT')
    # )

    # queryset = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value(' '), 'last_name')
    # )

    # queryset = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )

    # discounted_price = ExpressionWrapper(
    #     F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(
    #     discounted_price=discounted_price
    # )

    # queryset = Customer.objects.annotate(
    #     last_order_id=Max('order__id')
    # )

    # queryset = Collection.objects.annotate(
    #     products_count=Count('product')
    # )

    # queryset = Customer.objects.annotate(
    #     orders_count=Count('order')
    # ).filter(orders_count__gt=5)

    # queryset = Customer.objects.annotate(
    #     total_spent=Sum(
    #         F('order__orderitem__quantity') *
    #         F('order__orderitem__unit_price')
    #     )
    # )

    # queryset = Product.objects.annotate(
    #     total_sales=Sum(
    #         F('orderitem__quantity') * F('orderitem__unit_price')
    #     )
    # ).order_by('-total_sales')[:5]

    # queryset = TaggedItem.objects.get_tags_for(Product, 1)

    # collection = Collection(pk=11)
    # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()

    # Collection.objects.filter(pk=11).update(featured_product=1)

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    try:
        # send_mail('subject', 'message',
        #           'info@danarbuy.com', ['bob@danarbuy.com'])

        # mail_admins('subject', 'message', html_message='message')

        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'Bung Danar'}
        )
        message.send(['john@danarbuy.com'])
    except BadHeaderError:
        pass

    return render(request, 'hello.html', {
        'name': 'Bung Danar',
        # 'result': list(queryset)
    })
