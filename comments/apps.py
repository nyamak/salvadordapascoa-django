"""
Comments Apps
"""
###
# Libraries
###
from django.apps import AppConfig


###
# Config
###
class CommentsConfig(AppConfig):
    name = 'comments'

    def ready(self):
        import comments.signals
