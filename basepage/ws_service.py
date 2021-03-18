from product.serializers import *
from basepage.serializers import *


async def update_product(product):
    print('ID ID ID')
    print(product)
    print(product.id)
    group_name = ProductDetailSerializer(product).get_group_name()
    channel_layer = get_channel_layer()
    print('Обновление продукта')
    content = {
        "type": "UPDATE_PRODUCT",
        "payload": product.id,
    }
    await channel_layer.group_send(group_name, {
        "type": "notify",
        "content": content,
    })


async def update_categories(category):
    group_name = CategoriesListSerializer().get_group_name()
    channel_layer = get_channel_layer()

    content = {
        "type": "UPDATE_PRODUCT",
        "payload": category.id,
    }
    await channel_layer.group_send(group_name, {
        "type": "notify",
        "content": content,
    })