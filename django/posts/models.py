from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from markdown_deux import markdown
from slugify import slugify


from .utils import get_read_time
from .validators import validate_file_extensions

import os, shutil


def upload_location(instance, filename):
    return f'{instance.slug}/{filename}'


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field='width_field',
        height_field='height_field'
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField(max_length=500)
    attachment = models.FileField(
        validators=[validate_file_extensions],
        upload_to=upload_location,
        null=True,
        blank=True,
    )
    read_time = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='subscribed_for'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs = {'slug': str(self.slug)})

    class Meta:
        ordering = ['-created', '-updated']

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_attachment_ext(self):
        return os.path.splitext(self.attachment.path)[1]

    def get_attachment_filename(self):
        return self.attachment.name.split('/')[1]

    def remove_files(self):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, self.slug))


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance.content:
        html_string = instance.get_markdown()
        read_time = get_read_time(html_string)
        instance.read_time = read_time

    if instance.title:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_post_receiver, sender=Post)

def pre_delete_file_receiver(sender, instance, *args, **kwargs):
    instance.remove_files()

pre_delete.connect(pre_delete_file_receiver, sender=Post)
