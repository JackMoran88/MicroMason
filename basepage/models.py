import os
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import RegexValidator

from django.db.models import Model, CASCADE
from django.db.models import CharField, FloatField, TextField, FilePathField, PositiveIntegerField, SlugField, \
    EmailField
from django.db.models import DateField, BooleanField
from django.db.models import ManyToManyField, ForeignKey

from django.db.models import ImageField

from django.contrib.auth.models import UnicodeUsernameValidator, AbstractBaseUser, BaseUserManager, PermissionsMixin

from autoslug import AutoSlugField

from django.db.models import SET_NULL



class Option(Model):
    name = CharField(max_length=120, null=False)

    def __str__(self):
        return f"{self:id}: {self.name}"


class OptionParameter(Model):
    name = CharField(max_length=120, null=False)
    option = ForeignKey(Option, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id}: {self.name}"



class Category(Model):
    parent = ForeignKey("self", on_delete=CASCADE, null=True, blank=True, related_name='children')
    name = CharField(max_length=120, null=False)
    description = TextField(blank=True)
    main_image = ImageField("Изображение", upload_to="Categories/", blank=True)

    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)

    priority = BooleanField(default=False)

    def __str__(self):
        return f"{self.parent} => {self.id}: {self.name}"



class ProductImage(Model):
    image = ImageField(upload_to='ProductImages/', unique=True)

    class Meta:
        verbose_name_plural = 'Фото товаров'
        verbose_name = 'Фото товара'


class Product(Model):
    name = CharField(max_length=120, null=False)
    code = PositiveIntegerField(null=False)
    quantity = PositiveIntegerField(editable=True, default=0)
    price = FloatField(null=False)
    description = TextField(blank=True)
    main_image = ImageField("Изображение", upload_to="Products/", blank=True)

    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)

    category = ManyToManyField(Category, related_name='category')
    images = ManyToManyField(ProductImage, blank=True, related_name='images')
    options = ManyToManyField(OptionParameter,
                              through='OptionProduct',
                              through_fields=(
                                  "product",
                                  "option_parameter"
                              ),
                              blank=True)

    def __str__(self):
        return f"{self.id}: {self.name}"


class OptionProduct(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    option_parameter = ForeignKey(OptionParameter, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.option_parameter} in {self.product} = {self.quantity}"


class CustomerManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    # username_validator = UnicodeUsernameValidator()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+380991234567'.")

    email = EmailField('email address',
                       null=False,
                       unique=True)
    phone_number = CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True
    )
    birthday = DateField(blank=True, null=True)
    # remember = BooleanField(default=False)
    first_name = CharField(max_length=50, default='', blank=False, null=False)
    last_name = CharField(max_length=50, blank=False, null=False)

    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True


class Review(Model):
    author = ForeignKey(Customer, on_delete=CASCADE)
    text = TextField("Сообщение", max_length=5000)
    parent = ForeignKey(
        'self', verbose_name="Родитель", on_delete=SET_NULL, blank=True, null=True
    )
    product = ForeignKey(Product, verbose_name="product", on_delete=CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"