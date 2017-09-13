from django.conf import settings
from django.db import models

from regiclass.models import Lecture

__all__ = (
    'Review',
)


class Review(models.Model):
    lecture = models.ForeignKey(
        Lecture,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )
    curriculum_rate = models.IntegerField(
        default=0,
    )
    delivery_rate = models.IntegerField(
        default=0,
    )
    preparation_rate = models.IntegerField(
        default=0,
    )
    kindness_rate = models.IntegerField(
        default=0,
    )
    punctually_rate = models.IntegerField(
        default=0,
    )
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modify_date']

    def __str__(self):
        return '{}, {}, {}, {}, {}'.format(self.curriculum_rate, self.delivery_rate, self.preparation_rate, self.kindness_rate, self.punctually_rate)