import os
import binascii
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import RegexValidator

from django.db.models import Model, CASCADE
from django.db.models import CharField, FloatField, TextField, PositiveIntegerField, EmailField, DateTimeField, JSONField
from django.db.models import DateField, BooleanField
from django.db.models import ManyToManyField, ForeignKey

from django.db.models import ImageField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from autoslug import AutoSlugField

from django.db.models import SET_NULL, SmallIntegerField, Avg

from model_utils import FieldTracker
from asgiref.sync import async_to_sync, sync_to_async
from django.utils.html import mark_safe

import mptt
from mptt.models import MPTTModel, TreeForeignKey

from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.placeholder import OnStoragePlaceholderImage


# import product.models


class Category(MPTTModel):
    parent = TreeForeignKey("self", on_delete=CASCADE, null=True, blank=True, related_name='children')
    name = CharField(max_length=120, null=False, blank=True)
    description = TextField(blank=True)

    main_image = VersatileImageField(
        "Изображение",
        upload_to="Categories/",
        blank=True,
        ppoi_field='main_image_ppoi',
        placeholder_image=OnStoragePlaceholderImage(
            path='images/default/product/404.png'
        )
    )

    main_image_ppoi = PPOIField()

    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)

    priority = BooleanField(default=False)

    row = SmallIntegerField(null=True, blank=True)

    order_by = PositiveIntegerField(blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    tracker = FieldTracker(fields=('name',), )

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        has_changed = self.tracker.has_changed('name')
        if has_changed:
            from basepage.ws_service import update_categories
            async_to_sync(update_categories)(self)
            return ret

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"

    class MPTTMeta:
        # level_attr = 'mptt_level'
        order_insertion_by = ['name']


mptt.register(Category, order_insertion_by=['name'])




class CustomerManager(BaseUserManager):
    def create_user(self, email, first_name='', last_name='', password=None, **kwargs):


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

    class Meta:
        verbose_name = 'Пол пользователя'
        verbose_name_plural = 'Пола пользователя'

    def __str__(self):
        return f'{self.gender}'


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


    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

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
        # НЕ ТРОГАТь, задействуется при отображнии автора коментария!(Уже не трогал: 3)
        full_name = f"{self.id} - {self.get_full_name()}"
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
        super(Customer, self).save(force_insert, force_update, using, update_fields)


class AnonymousCustomer(Model):
    token = CharField(max_length=40)
    last_update = DateField(auto_now_add=True, )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Аноним"
        verbose_name_plural = "Анонимые пользователи"

    def __str__(self):
        return f'{self.id} - {self.last_update}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = binascii.hexlify(os.urandom(20)).decode()
        super(AnonymousCustomer, self).save(*args, **kwargs)

class RatingStar(Model):
    value = SmallIntegerField("Значение", default=0)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Review(MPTTModel):
    author = ForeignKey(Customer, on_delete=CASCADE, blank=False)
    star = ForeignKey(RatingStar, on_delete=CASCADE, verbose_name="Звезда", null=True, blank=True)

    text = TextField("Коментарий", max_length=5000, blank=True, null=True)
    advantages = TextField("Достоинства", max_length=2500, blank=True, null=True)
    disadvantages = TextField("Недостатки", max_length=2500, blank=True, null=True)

    parent = TreeForeignKey(
        "self",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name="Родитель",
        related_name='children',
    )

    product = ForeignKey(
        'product.Product',
        on_delete=CASCADE,
        verbose_name="Товар",
        related_name="reviews",
        blank=False,
    )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # Не добовлять автора, будет рекурсивный запрос
    tracker = FieldTracker(fields=('star', 'text', 'advantages', 'disadvantages',), )

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        has_changed = self.tracker.changed()
        if has_changed:
            from basepage.ws_service import update_product
            async_to_sync(update_product)(self.product)
            return ret

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Wish(Model):
    customer = ForeignKey(Customer, on_delete=CASCADE, related_name='wish', null=True, blank=True)
    anonymous_customer = ForeignKey(AnonymousCustomer, on_delete=SET_NULL, null=True, blank=True)

    product = ForeignKey('product.Product', on_delete=CASCADE, related_name='product', )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Список желаемого'
        verbose_name_plural = 'Списки желаемого'

    def __str__(self):
        return f"User: {self.customer} ,product #{self.product}"

class Compare(Model):
    customer = ForeignKey(Customer, on_delete=CASCADE, null=True, blank=True)
    anonymous_customer = ForeignKey('AnonymousCustomer', on_delete=SET_NULL, null=True, blank=True)

    product = ForeignKey('product.Product', on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Список сравнениея'
        verbose_name_plural = 'Списки сравнений'

    def __str__(self):
        return f"User: {self.customer} ,product #{self.product}"
