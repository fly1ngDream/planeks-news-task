from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save

from posts.models import Post


class CommentManager(models.Manager):
    '''
    Comment model manager
    '''

    def all(self):
        '''
        Rewrites all function to show only comments that dont have a parent
        '''
        qs = super().filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        '''
        Filter comments by a parent
        '''
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super().filter(parent_pk=instance.pk).filter(parent=None)
        return qs

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    post = models.ForeignKey(
        Post,
        default=1,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        content = self.content[:80]
        return f'{content}...' if len(self.content) > 80 else self.content

    def children(self):
        '''
        Returns the children of the comment
        '''
        return Comment.objects.filter(parent=self)

    def get_absolute_url(self):
        '''
        Returns an absolute url to a comment
        '''
        return reverse('comments:comment_detail', kwargs = {'pk': str(self.pk)})

    @property
    def is_parent(self):
        '''
        Check if comment is parent
        '''
        if self.parent is not None:
            return False
        else:
            return True
