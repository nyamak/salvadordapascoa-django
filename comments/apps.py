"""
Comments Apps
"""
###
# Libraries
###
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

###
# Config
###
class CommentsConfig(AppConfig):
    name = 'comments'
    verbose_name = _('Comentários')

    def ready(self):
        import comments.signals
