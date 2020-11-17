import os
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import RegexValidator

from django.db.models import Model, CASCADE
from django.db.models import CharField, FloatField, TextField, PositiveIntegerField, EmailField, DateTimeField
from django.db.models import DateField, BooleanField
from django.db.models import ManyToManyField, ForeignKey

from django.db.models import ImageField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from autoslug import AutoSlugField

from django.db.models import SET_NULL, SmallIntegerField, Avg

from model_utils import FieldTracker
from asgiref.sync import async_to_sync, sync_to_async
from django.utils.html import mark_safe


class Category(Model):
    parent = ForeignKey("self", on_delete=CASCADE, null=True, blank=True, related_name='children')
    name = CharField(max_length=120, null=False, blank=True)
    description = TextField(blank=True)
    main_image = ImageField("Изображение", upload_to="Categories/", blank=True)

    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)

    priority = BooleanField(default=False)

    tracker = FieldTracker(fields=('name',), )

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        has_changed = self.tracker.has_changed('name')
        if has_changed:
            from .views import update_categories
            async_to_sync(update_categories)(self)
            return ret

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.parent} => {self.id}: {self.name}"


class Option(Model):
    name = CharField(max_length=225)

    def __str__(self):
        return f" {self.id}: {self.name}"


class OptionProduct(Model):
    name = CharField(max_length=225)
    product = ForeignKey('Product',
                         on_delete=CASCADE,
                         null=True,
                         blank=True, related_name='options')
    parameter = ForeignKey(Option, on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return f" {self.id}: {self.parameter} - {self.name}"


class Product(Model):
    name = CharField(max_length=120, null=False)
    code = PositiveIntegerField(null=False)
    quantity = PositiveIntegerField(editable=True, default=0)
    price = FloatField(null=False)
    description = TextField(blank=True)
    main_image = ImageField("Изображение", upload_to="Products/", blank=True, default='images/default/product/404.png')

    # options = ManyToManyField(OptionProduct,
    #                           null=True,
    #                           blank=True,
    #                           related_name='Характеристики', )

    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)

    category = ManyToManyField(Category, related_name='category')

    tracker = FieldTracker(fields=('name', 'code', 'quantity', 'price', 'description', 'main_image',), )

    def image_tag(self):
        return mark_safe(
            '<img src="/media/%s" width="75" height="75" />' % (self.main_image)
        )

    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        has_changed = self.tracker.changed()
        if has_changed:
            from .views import update_product
            async_to_sync(update_product)(self)
            return ret

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.id}: {self.name}"


class ProductImage(Model):
    product_id = ForeignKey('Product', on_delete=CASCADE, related_name='images')
    image = ImageField(upload_to='ProductImages/', unique=True)

    class Meta:
        verbose_name_plural = 'Фото товаров'
        verbose_name = 'Фото товара'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.image))

    image_tag.short_description = 'Image'


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


class CustomerGender(Model):
    gender = CharField(max_length=20, verbose_name='Пол', null=True, blank=True)


class Customer(AbstractBaseUser, PermissionsMixin):
    # username_validator = UnicodeUsernameValidator()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+380991234567'.")
    email = EmailField('email address',
                       null=False,
                       unique=True)
    phone_number = CharField(validators=[phone_regex], max_length=17, blank=True)
    birthday = DateField(blank=True, null=True)
    first_name = CharField(max_length=50, default='', blank=False, null=False)
    last_name = CharField(max_length=50, blank=False, null=False)
    middle_name = CharField(max_length=50, default='', blank=True)
    gender = ForeignKey(CustomerGender, on_delete=CASCADE, null=True, blank=True)

    # cart = ForeignKey(Cart, on_delete=SET_NULL, null=True)

    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        # НЕ ТРОГАТь, задействуется при отображнии автора коментария!(Уже не трогал: 1)
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_full_name(self):
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # try:
        #     print(self.cart)
        #     if self.cart.pk == 'null':
        #         self.cart = Cart()
        #         self.cart.save()
        # except:
        #     self.cart = Cart()
        #     self.cart.save()
        super(Customer, self).save(force_insert, force_update, using, update_fields)


class AnonymousCustomer(Model):
    # token = CharField(max_length=25)
    last_update = DateField(auto_now_add=True, )

    class Meta:
        verbose_name = "Аноним"
        verbose_name_plural = "Анонимые пользователи"


class Cart(Model):
    customer = ForeignKey(Customer, on_delete=CASCADE, null=True, blank=True)
    anonymous_customer = ForeignKey(AnonymousCustomer, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f'Корзина #{self.id}'


class CartProduct(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = "Товар корзины"
        verbose_name_plural = "Товары корзины"

    def __str__(self):
        return f"Корзина #{self.cart.id} - {self.product}"


class Review(Model):
    author = ForeignKey(Customer, on_delete=CASCADE, blank=False, null=False)
    text = TextField("Сообщение", max_length=5000, blank=True, null=True)
    parent = ForeignKey(
        'self', verbose_name="Родитель", on_delete=SET_NULL, blank=True, null=True, related_name='children'
    )
    product = ForeignKey(Product, verbose_name="product", on_delete=CASCADE, related_name="reviews", blank=False)

    def __str__(self):
        return f"{self.author} - {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class RatingStar(Model):
    value = SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(Model):
    author = ForeignKey(Customer, on_delete=CASCADE, blank=False)
    star = ForeignKey(RatingStar, on_delete=CASCADE, verbose_name="Звезда", )

    text = TextField("Коментарий", max_length=5000, blank=True, null=True)
    advantages = TextField("Достоинства", max_length=2500, blank=True, null=True)
    disadvantages = TextField("Недостатки", max_length=2500, blank=True, null=True)
    parent = ForeignKey(
        'self', verbose_name="Родитель", on_delete=SET_NULL, blank=True, null=True, related_name='children'
    )

    product = ForeignKey(
        Product,
        on_delete=CASCADE,
        verbose_name="Товар",
        related_name="ratings",
        blank=False,
    )

    created_at = DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Wish(Model):
    customer = ForeignKey(Customer, on_delete=CASCADE, related_name='wish')
    product = ForeignKey(Product, on_delete=CASCADE, related_name='product', )

    def __str__(self):
        return f"User: {self.customer} ,product #{self.product}"
