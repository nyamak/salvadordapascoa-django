"""
Comments Models
"""
###
# Libraries
###

from django.utils.translation import gettext_lazy as _
from django.db import models

from accounts.models import User
from helpers.models import TimestampModel

###
# Choices
###


###
# Querysets
###


###
# Models
###


class Comment(TimestampModel):

    author = models.ForeignKey(
        User,
        verbose_name=_('autor'),
        null=True,
        related_name='comments',
        on_delete=models.SET_NULL,
    )

    body = models.TextField(
        verbose_name=_('corpo'),
        max_length=2048,
    )

    def __str__(self):
        return f'{self.author.get_full_name() if self.author else "Anônimo"}: {self.body[:25]}'
