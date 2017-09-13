from django.db import models

from regiclass.models import Lecture

__all__ = (
    'Curriculum',
)


class Curriculum(models.Model):
    lecture = models.ForeignKey(
        Lecture,
        related_name='curriculum',
        on_delete=models.CASCADE,
    )
    curriculum_photo = models.ImageField(
        upload_to='class/images/%Y/%m/%d',
        blank=True,
        null=True,
    )
    curriculum_desc = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
