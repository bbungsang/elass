from django.conf import settings
from django.db import models

from regiclass.models import Lecture


class Enrollment(models.Model):
    class Meta:
        unique_together = (
            ('user', 'lecture'),
        )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name='enrollment_lecture',
    )

    location = models.CharField(max_length=24, blank=True)
    class_day = models.CharField(max_length=8, blank=True)
    class_time = models.CharField(max_length=24, blank=True)

    LEVEL_BEGINNER = 'beginner'
    LEVEL_INTERMEDIATE = 'intermediate'
    LEVEL_ADVANCED = 'advanced'

    LEVEL_CHOICE = (
        (LEVEL_BEGINNER, '입문자'),
        (LEVEL_INTERMEDIATE, '초중급자'),
        (LEVEL_ADVANCED, '상급자'),
    )

    level = models.CharField(
        max_length=12,
        choices=LEVEL_CHOICE,
        blank=True,
    )

    career = models.CharField(max_length=36, blank=True,)
    to_tutor = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,)
    modified_at = models.DateTimeField(auto_now=True,)

    PAY_METHOD_CREDIT = 'credit'
    PAY_METHOD_BANKBOOK = 'bankbook'

    PAY_METHOD_CHOICE = (
        (PAY_METHOD_CREDIT, '신용카드'),
        (PAY_METHOD_BANKBOOK, '무통장입금'),
    )

    pay_method = models.CharField(
        max_length=12,
        choices=PAY_METHOD_CHOICE,
        blank=True,
    )

    remitter = models.CharField(
        max_length=24,
        blank=True,
    )
    due_date = models.CharField(max_length=36, blank=True, null=True)

