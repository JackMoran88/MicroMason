import os
from django.conf import settings
from django.utils.text import slugify

from django.db.models import Model, CASCADE
from django.db.models import CharField, FloatField, TextField, FilePathField, PositiveIntegerField, SlugField
from django.db.models import ManyToManyField, ForeignKey


def images_path():
    return os.path.join(settings.MEDIA_ROOT, "images")


class Option(Model):
    name = CharField(max_length=120, null=False)

    def __str__(self):
        return f"{self:id}: {self.name}"


class OptionParameter(Model):
    name = CharField(max_length=120, null=False)
    option = ForeignKey(Option, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Image(Model):
    src = FilePathField(path=images_path, null=False)

    def __str__(self):
        return f"{self.id}: {self.src}"


class Category(Model):
    parent = ForeignKey("self", on_delete=CASCADE, null=True, blank=True)
    name = CharField(max_length=120, null=False)
    description = TextField(blank=True)

    slug = SlugField(blank=True, allow_unicode=True)

    def __str__(self):
        return f"{self.parent} => {self.id}: {self.name}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.slug == "":
            self.slug = slugify(self.name, allow_unicode=True)

        super(Category, self).save(force_insert, force_update, using,
                                   update_fields)


class Product(Model):
    name = CharField(max_length=120, null=False)
    code = PositiveIntegerField(null=False)
    quantity = PositiveIntegerField(editable=True, default=0)
    price = FloatField(null=False)
    description = TextField(blank=True)
    main_image = FilePathField(path=images_path)

    slug = SlugField(blank=True, allow_unicode=True)

    category = ManyToManyField(Category)
    images = ManyToManyField(Image, blank=True)
    options = ManyToManyField(OptionParameter,
                              through='OptionProduct',
                              through_fields=(
                                  "product",
                                  "option_parameter"
                              ),
                              blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # self.quantity.editable = False

        if self.slug == "":
            self.slug = slugify(self.name, allow_unicode=True)

        super(Product, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.id}: {self.name}"


class OptionProduct(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    option_parameter = ForeignKey(OptionParameter, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.option_parameter} in {self.product} = {self.quantity}"
