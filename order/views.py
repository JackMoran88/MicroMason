from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, viewsets
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from basepage.models import *


class OrderViewSet(viewsets.ViewSet):
    def list(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            orders = Order.objects.all().annotate(
                total=Sum(F('order_products__product__price') * F('order_products__quantity'),
                          output_field=FloatField()),
                qty=Sum(F('order_products__quantity'))
            ).filter(customer_id=user.id)
            serializer = OrderDetailSerializer(orders, many=True)
            return Response(serializer.data)

        elif 'anonymous' in user.keys():
            user = user['anonymous']
            order = Order.objects.annotate(
                total=Sum(F('order_products__product__price') * F('order_products__quantity'),
                          output_field=FloatField()),
                qty=Sum(F('order_products__quantity'))
            )
            order = get_object_or_404(order, anonymous_customer_id=user.id)

            serializer = OrderDetailSerializer(order, many=True)
            return Response(serializer.data)

        else:
            return Response(status=400)

    def create(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            data = {
                'customer': user,
                'payment_method': 0,
            }
            order = Order.objects.create(
                customer=data.get('customer'),
                anonymous_customer=data.get('anonymous_customer'),
                payment_method=data.get('payment_method'),
            )
            order.save()


            cart_products = CartProduct.objects.filter(cart__customer_id=user.id)

            OrderProduct.objects.filter(order__customer_id=user.id, order_id=order.id).delete()
            for product in cart_products:
                order_product, _ = OrderProduct.objects.update_or_create(
                    order=order,
                    product=product.product,
                    quantity=product.quantity
                )
                order_product.save()

            Cart.objects.filter(customer_id=user.id).delete()
            return Response(status=201)

        elif 'anonymous' in user.keys():
            user = user['anonymous']
            data = {
                'anonymous_customer': user.id,
                'payment_method': 0,
            }
            order = OrderCreateSerializer(data=data)
            if order.is_valid(raise_exception=True):
                order.save()

                order = Order.objects.get(anonymous_customer_id=user.id)
                cart_products = CartProduct.objects.filter(cart__anonymous_customer_id=user.id)

                OrderProduct.objects.filter(order__anonymous_customer_id=user.id).delete()
                for product in cart_products:
                    order_product, _ = OrderProduct.objects.update_or_create(
                        order=order,
                        product=product.product,
                        quantity=product.quantity
                    )
                    order_product.save()
                return Response(status=201)
        else:
            return Response(status=400)
