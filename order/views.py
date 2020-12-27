from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, viewsets
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from basepage.models import *
from cart.models import *


class OrderViewSet(viewsets.ViewSet):
    def list(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            orders = Order.objects.all().annotate(
                total=Sum(F('order_products__product__price') * F('order_products__quantity'),
                          output_field=FloatField()),
                qty=Sum(F('order_products__quantity'))
            ).filter(customer_id=user.id).order_by('-created_at')
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

            payment_method = Payment.objects.get(id=request.data.get('payment'))
            shipping_method = Shipping.objects.get(id=request.data.get('shipping'))
            address = Address.objects.get(id=request.data.get('address'))
            data = {
                'customer': user,
                'payment_method': payment_method,
                'shipping': shipping_method,
                'address': address,
            }
            order = Order.objects.create(
                customer=data.get('customer'),
                payment_method=data.get('payment_method'),
                shipping=data.get('shipping'),
                address=data.get('address'),
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

            queryset = Order.objects.get(id=order.id)
            serializer = OrderDetailSerializer(queryset)
            return Response(serializer.data, status=201)

        else:
            return Response(status=400)


class AddressViewSet(viewsets.ViewSet):
    def list(self, request):
        user = get_user(request)
        user = user['customer']

        queryset = Address.objects.filter(customer=user)

        serializer = AddressDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']

            Address.objects.update_or_create(
                id=request.data.get('id'),
                defaults={
                    'customer': user,
                    'first_name': request.data.get('first_name'),
                    'last_name': request.data.get('last_name'),
                    'email': request.data.get('email'),
                    'phone_number': request.data.get('phone_number'),
                    'address': request.data.get('address'),
                    'postal_code': request.data.get('postal_code'),
                    'city': request.data.get('city'),
                }

            )
            return Response(status=201)

        else:
            return Response(status=400)

    def delete(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            Address.objects.get(customer=user, id=request.data.get('id')).delete()
            return Response(status=200)
        else:
            return Response(status=400)


class ShippingViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Shipping.objects.all()
        serializer = ShippingDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Payment.objects.all()
        serializer = PaymentDetailSerializer(queryset, many=True)
        return Response(serializer.data)
