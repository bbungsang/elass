from django.db import models

from regiclass.models import Lecture

__all__ = (
    'LecturePhoto',
)


class LecturePhoto(models.Model):
    lecture = models.ForeignKey(
        Lecture,
        related_name='lecture_photos',
        on_delete=models.CASCADE,
    )
    lecture_photo = models.ImageField(
        upload_to='class/images/%Y/%m/%d',
    )
