from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

MyUser = get_user_model()


class Tutor(models.Model):
    CERT_TYPE_UNIV = 'univ'
    CERT_TYPE_GRAD = 'grad'
    CERT_TYPE_IDENTITY = 'identity'

    CERT_TYPE_CHOICE = (
        (CERT_TYPE_UNIV, '대학인증'),
        (CERT_TYPE_GRAD, '대학원인증'),
        (CERT_TYPE_IDENTITY, '신분증인증'),
    )

    STATUS_TYPE_ING = 'ing'
    STATUS_TYPE_GRADUATION = 'graduation'
    STATUS_TYPE_COMPLETE = 'complete'
    STATUS_TYPE_CHOICE = (
        ('ing', '재학'),
        ('graduation', '졸업'),
        ('complete', '수료'),
    )

    author = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='myuser',
    )

    cert_type = models.CharField(
        max_length=8,
        choices=CERT_TYPE_CHOICE,
    )

    school = models.CharField(
        max_length=20,
        blank=True,
    )

    major = models.CharField(
        max_length=20,
        null=True,
    )

    status_type = models.CharField(
        max_length=10,
        choices=STATUS_TYPE_CHOICE,
        null=True,
    )

    identification = models.ImageField(
        upload_to='user/%Y/%m/%d',
        null=True,
    )

    ##
    # 앱에서 요구하는 필드
    ##

    # how_to_know = models.CharField(
    #     max_length=100,
    # )
    # age = models.CharField(
    #     max_length=3,
    # )
    # class_talent = models.CharField(
    #     max_length=20,
    #     null=True,
    # )
    # class_location = models.CharField(
    #     max_length=20,
    #     null=True,
    # )