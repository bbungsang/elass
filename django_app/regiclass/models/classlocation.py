from django.db import models

from regiclass.models import Lecture

__all__ = (
    'ClassLocation',
)


class ClassLocation(models.Model):
    LOCATION_DIRECT = 'direct'
    LOCATION_CUSTOM = 'custom'

    TYPE_YES = 'yes'
    TYPE_NO = 'no'

    WEEKDAY_MON = 'mon'
    WEEKDAY_TUE = 'tue'
    WEEKDAY_WED = 'wed'
    WEEKDAY_THU = 'thu'
    WEEKDAY_FRI = 'fri'
    WEEKDAY_SAT = 'sat'
    WEEKDAY_SUN = 'sun'

    LOCATION_OPTION_CHOICE = (
        (LOCATION_DIRECT, '협의후결정'),
        (LOCATION_CUSTOM, '직접입력'),
    )

    ETC_TYPE_CHOICE = (
        (TYPE_YES, '예'),
        (TYPE_NO, '아니오'),
    )

    WEEKDAY_CHOICE = (
        (WEEKDAY_MON, '월'),
        (WEEKDAY_TUE, '화'),
        (WEEKDAY_WED, '수'),
        (WEEKDAY_THU, '목'),
        (WEEKDAY_FRI, '금'),
        (WEEKDAY_SAT, '토'),
        (WEEKDAY_SUN, '일'),
    )

    lecture = models.ForeignKey(
        Lecture,
        related_name='locations',
        on_delete=models.CASCADE,
    )
    location1 = models.CharField(
        max_length=20,
    )
    location2 = models.CharField(
        max_length=20,
    )
    location_option = models.CharField(
        max_length=6,
        choices=LOCATION_OPTION_CHOICE,
        default=LOCATION_DIRECT,
    )
    location_detail = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    location_etc_type = models.CharField(
        max_length=3,
        choices=ETC_TYPE_CHOICE,
        default=TYPE_YES,
    )
    location_etc_text = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    class_weekday = models.CharField(
        max_length=3,
        choices=WEEKDAY_CHOICE,
        default=WEEKDAY_MON,
    )
    class_time = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
