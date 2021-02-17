from django.core.management.base import BaseCommand

from product.models import Product
from basepage.models import Category
from category.models import Filter
import copy


def remove_dublicates(arr, parameter):
    # `return [dict(t) for t in {tuple(d.items()) for d in arr}]`
    done = set()
    result = []
    for d in arr:
        if d[parameter] not in done:
            done.add(d[parameter])  # note it down for further iterations
            result.append(d)
    return result


def log(msg, value):
    pass
    # print(msg)
    # print(value)


def filters_by_default():
    filters = [
        ['Стоимость', '0', 'prices', '', '', '', '', '', True]
    ]
    for filter in filters:
        data = {
            'name': filter[0],
            'type': filter[1],
            'request_name': filter[2],
            'model': filter[3],
            'model_parameter_id': filter[4],
            'filter': filter[5],
            'sub_model': filter[6],
            'sub_filter': filter[7],
            'state': filter[8]
        }
        instance = Filter.objects.create(**data)
        instance.category.set(Category.objects.all().values_list('id', flat=True))


def filters_by_options():
    products = Product.objects.all()

    #   parameters
    parameters = products.values('id', 'options__parameter__id', 'options__parameter__name',
                                 'options__parameter__category', 'options__parameter__category__name',
                                 'options__parameter__optionproduct__name', 'options__parameter__request_name')
    all_parameters = copy.deepcopy(parameters)
    parameters = remove_dublicates(parameters, 'options__parameter__name')
    #   names
    names = []
    for parameter in parameters:
        names.append(parameter['options__parameter__name'])

    log('Names', names)
    #   request names
    request_names = []
    for parameter in parameters:
        request_names.append(parameter['options__parameter__request_name'])

    log('Request names', request_names)
    #   Model parameters
    model_parameters = []
    for parameter in parameters:
        model_parameters.append(parameter['options__parameter__id'])

    log('Model parameters', model_parameters)
    #   Filters
    filters = []
    for parameter in parameters:
        filters.append({'id': parameter['options__parameter__id']})

    log('Filters', filters)
    #   Sub filters
    sub_filter = []
    for parameter in parameters:
        sub_filter.append({'options__parameter_id': parameter['options__parameter__id']})

    log('Sub filters', sub_filter)
    #   Categories
    categories = []
    for parameter in model_parameters:
        categories.append(
            list(set(products.filter(options__parameter_id=parameter).values_list('category_id', flat=True))))

    log('Categories', categories)

    for num, filter in enumerate(parameters):
        data = {
            'name': names[num],
            'type': 0,
            'request_name': request_names[num],
            'model': 'Option',
            'model_parameter_id': model_parameters[num],
            'filter': filters[num],
            'sub_model': 'Product',
            'sub_filter': sub_filter[num],
            'state': True
        }
        instance = Filter.objects.create(
            **data
        )
        instance.category.set(categories[num])


class Command(BaseCommand):
    help = 'Спарсить фильтры'

    def handle(self, **options):
        Filter.objects.all().delete()
        filters_by_default()
        filters_by_options()
