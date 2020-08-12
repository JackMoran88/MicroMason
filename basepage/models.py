import os
from django.conf import settings

from django.db.models import Model, CASCADE
from django.db.models import CharField, FloatField, TextField, FilePathField, IntegerField, PositiveIntegerField
from django.db.models import ManyToManyField, ForeignKey


def images_path():
    return os.path.join(settings.MEDIA_ROOT, "images")


class Option(Model):
    name = CharField(max_length=120, null=False)


class OptionParameter(Model):
    name = CharField(max_length=120, null=False)
    option = ForeignKey(Option, on_delete=CASCADE)


class Image(Model):
    src = FilePathField(path=images_path, null=False)


class Category(Model):
    parent = ForeignKey("self", on_delete=CASCADE)
    name = CharField(max_length=120, null=False)
    description = TextField()


class Product(Model):
    name = CharField(max_length=120, null=False)
    code = PositiveIntegerField(null=False)
    quantity = PositiveIntegerField(editable=True, default=0)
    price = FloatField(null=False)
    description = TextField()
    main_image = FilePathField(path=images_path)

    category = ManyToManyField(Category)
    images = ManyToManyField(Image)
    options = ManyToManyField(OptionParameter,
                              through='OptionProduct',
                              through_fields=(
                                  "product",
                                  "option_parameter"
                              ))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):

        # self.quantity.editable = False
        super(Product, self).save(*args, **kwargs)


class OptionProduct(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    option_parameter = ForeignKey(OptionParameter, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=0)
