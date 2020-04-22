"""
Seller Models
"""
###
# Libraries
###

import uuid

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from helpers.models import TimestampModel
from helpers.s3 import UploadFileTo
from seller.constants import STATE_CHOICES, FRIENDS, INSTAGRAM, FACEBOOK, TWITTER, OTHERS, TELEPHONE_NUMBER_REGEX

###
# Choices
###

REFERRALS_CHOICES = [
    (FRIENDS, _('Amigos')),
    (INSTAGRAM, _('Instagram')),
    (FACEBOOK, _('Facebook')),
    (TWITTER, _('Twitter')),
    (OTHERS, _('Outros')),
]


###
# Querysets
###


###
# Models
###


class Seller(TimestampModel):

    UPLOAD_TO = 'sellers'

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        verbose_name=_('usuário'),
        on_delete=models.CASCADE,
        related_name='seller',
    )

    name = models.CharField(
        verbose_name=_('nome'),
        max_length=64,
    )

    description = models.TextField(
        verbose_name=_('descrição'),
        max_length=1024,
    )

    # Location fields
    neighborhood = models.CharField(
        verbose_name=_('bairro'),
        max_length=64,
    )

    city = models.CharField(
        verbose_name=_('cidade'),
        max_length=64,
    )

    state = models.CharField(
        choices=STATE_CHOICES,
        verbose_name=_('estado'),
        max_length=2,
    )

    # Means fields
    delivery_means = models.ManyToManyField(
        'DeliveryMean',
        verbose_name=_('meios de entrega'),
        blank=False,
        related_name='sellers',
    )

    order_means = models.ManyToManyField(
        'OrderMean',
        verbose_name=_('meios de pedido'),
        blank=False,
        related_name='sellers',
    )

    # Contact fields
    telephone_number = models.CharField(
        verbose_name=_('número de telefone'),
        validators=[validators.RegexValidator(TELEPHONE_NUMBER_REGEX), ],
        max_length=24,
    )

    whatsapp_number = models.CharField(
        verbose_name=_('número do Whatsapp'),
        validators=[validators.RegexValidator(TELEPHONE_NUMBER_REGEX), ],
        max_length=24,
        blank=True,
        null=True,
    )

    instagram_profile = models.CharField(
        verbose_name=_('perfil do Instagram'),
        max_length=32,
        validators=[validators.RegexValidator(r'^@(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$'), ],
        unique=True,
    )

    ifood_url = models.URLField(
        verbose_name=_('link do iFood'),
        blank=True,
        null=True,
    )

    uber_eats_url = models.URLField(
        verbose_name=_('link do Uber Eats'),
        blank=True,
        null=True,
    )

    rappi_url = models.URLField(
        verbose_name=_('link do Rappi'),
        blank=True,
        null=True,
    )

    site_url = models.URLField(
        verbose_name=_('link do site'),
        blank=True,
        null=True,
    )

    # Image Field
    cover_image = models.ImageField(
        verbose_name=_('foto de capa'),
        upload_to=UploadFileTo(UPLOAD_TO, 'cover'),
        null=True,
    )

    legacy_cover_image = models.URLField(
        verbose_name=_('foto de capa legado'),
        null=True,
        blank=True
    )

    # Misc
    referrals = models.CharField(
        choices=REFERRALS_CHOICES,
        verbose_name=_('como você nos achou'),
        max_length=16,
        null=True,
        blank=True,
    )

    is_approved = models.BooleanField(
        default=False,
        verbose_name=_('aprovado'),
    )

    def __str__(self):
        return f'{self.name} ({self.city + " - " + self.state})'

    def save(self, *args, **kwargs):
        if not (self.cover_image or self.legacy_cover_image):
            raise ValidationError('Vendedor deve ter algum modo de foto de capa.')
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('vendedor')
        verbose_name_plural = _('vendedores')


class ProductImage(TimestampModel):

    UPLOAD_TO = 'products'

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    seller = models.ForeignKey(
        Seller,
        verbose_name=_('vendedor'),
        related_name='product_images',
        on_delete=models.CASCADE,
    )

    order = models.SmallIntegerField(
        verbose_name=_('ordem'),
        null=True,
        blank=True,
    )

    image = models.ImageField(
        verbose_name=_('foto'),
        upload_to=UploadFileTo(UPLOAD_TO, 'image'),
        null=True,
    )

    legacy_image = models.URLField(
        verbose_name=_('imagem legado'),
        blank=True,
        null=True,
        help_text=_('Link do Drive, para o processo de inscrição antigo')
    )

    def save(self, *args, **kwargs):
        if not (self.image or self.legacy_image):
            raise ValidationError('Imagem de produto deve ter algum modo de foto.')
        return super().save(*args, **kwargs)


class Mean(TimestampModel):

    name = models.CharField(
        verbose_name=_('nome'),
        unique=True,
        max_length=32,
    )

    slug = models.SlugField(
        verbose_name=_('identificador'),
        max_length=32,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True


class OrderMean(Mean):

    class Meta:
        verbose_name = _('meio de pedir')
        verbose_name_plural = _('meios de pedir')


class DeliveryMean(Mean):

    class Meta:
        verbose_name = _('meio de entrega')
        verbose_name_plural = _('meios de entrega')
