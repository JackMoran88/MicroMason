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
            queryset = Order.objects.all().annotate(
                total=Sum(F('order_products__product__price') * F('order_products__quantity'),
                          output_field=FloatField()),
                qty=Sum(F('order_products__quantity'))
            ).filter(customer_id=user.id).order_by('-created_at')
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            queryset = Order.objects.annotate(
                total=Sum(F('order_products__product__price') * F('order_products__quantity'),
                          output_field=FloatField()),
                qty=Sum(F('order_products__quantity'))
            )
            queryset = get_object_or_404(queryset, anonymous_customer_id=user.id)
        else:
            return Response(status=400)

        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = get_user(request)
        payment_method = get_object_or_404(Payment, id=request.data.get('payment'))
        shipping_method = get_object_or_404(Shipping, id=request.data.get('shipping'))
        address = get_object_or_404(Address, id=request.data.get('address'))
        data = {
            'payment_method': payment_method,
            'shipping': shipping_method,
            'address': address,
        }
        if 'customer' in user.keys():
            user = user['customer']
            data['customer'] = user

            order = Order.objects.create(**data)
            order.save()

            cart_products = CartProduct.objects.filter(cart__customer=user)

            OrderProduct.objects.filter(order__customer=user, order=order).delete()

            for item in cart_products:
                order_product, _ = OrderProduct.objects.update_or_create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
                order_product.save()

            Cart.objects.filter(customer=user).delete()

        elif 'anonymous' in user.keys():
            user = user['anonymous']
            data['anonymous_customer'] = user
            order = Order.objects.create(**data)
            order.save()

            cart_products = CartProduct.objects.filter(cart__anonymous_customer=user)

            OrderProduct.objects.filter(order__customer_id=user.id, order_id=order.id).delete()

            for item in cart_products:
                order_product, _ = OrderProduct.objects.update_or_create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
                order_product.save()

            Cart.objects.filter(anonymous_customer=user).delete()
        else:
            return Response(status=400)

        queryset = Order.objects.get(id=order.id)
        serializer = OrderDetailSerializer(queryset)
        return Response(serializer.data, status=201)


class AddressViewSet(viewsets.ViewSet):
    def list(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            queryset = Address.objects.filter(customer=user)
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            queryset = Address.objects.filter(anonymous_customer=user)
        else:
            return Response(status=400)

        serializer = AddressDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = get_user(request)
        data = {
            'id': request.data.get('id'),
            'defaults': {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'email': request.data.get('email'),
                'phone_number': request.data.get('phone_number'),
                'address': request.data.get('address'),
                'postal_code': request.data.get('postal_code'),
                'city': request.data.get('city'),
            }
        }
        if 'customer' in user.keys():
            user = user['customer']
            data['defaults']['customer'] = user
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            data['defaults']['anonymous_customer'] = user
        else:
            return Response(status=400)

        Address.objects.update_or_create(**data)
        return Response(status=201)

    def delete(self, request):
        user = get_user(request)
        data = {
            'id': request.data.get('id'),
        }
        if 'customer' in user.keys():
            user = user['customer']
            data['customer'] = user
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            data['anonymous_customer'] = user
        else:
            return Response(status=400)
        Address.objects.get(**data).delete()
        return Response(status=200)


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
