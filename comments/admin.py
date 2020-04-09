"""
Comments admin
"""
###
# Libraries
###

from django.contrib import admin

from comments.models import Comment

###
# Inline Admin Models
###


###
# Main Admin Models
###


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_at')
