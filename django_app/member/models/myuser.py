from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models

from rest_framework.authtoken.models import Token
from utils.fields.custom_image_fields import CustomImageField

__all__ = (
    # 'MyUserManager',
    'MyUser',
)


class MyUserManager(DefaultUserManager):
    def get_or_create_facebook_user(self, user_info):
        username = '{}_{}_{}'.format(
            self.model.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            user_info['id'],
        )
        user, user_created = self.get_or_create(
            username=username,
            email=user_info.get('email'),
            user_type=self.model.USER_TYPE_FACEBOOK,
            defaults={
                'email': user_info.get('email', ''),
                'my_photo': user_info['picture']['data'].get('url', '뭥미'),
            }
        )
        return user


class MyUser(AbstractUser):
    # def __init__(self, *args, **kwargs):
    #     super(MyUser, self).__init__(*args, **kwargs)
    #     self.username = models.CharField(
    #         max_length=300,
    #     )

    username = models.CharField(
        max_length=300,
        unique=True,
    )

    USERNAME_FIELD = 'username'

    my_photo = CustomImageField(
        upload_to='user/%Y/%m/%d',
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=13,
        blank=True,
    )

    name = models.CharField(
        max_length=12,
        blank=True,
    )

    nickname = models.CharField(
        max_length=24,
        blank=True
    )

    ##
    # 유저타입. 기본은 Django, 페이스북 로그인 시 USER_TYPE_FACEBOOK 값을 갖는다.
    ##
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=USER_TYPE_DJANGO)

    # enrollments = models.ManyToManyField(
    #     'regiclass.Lecture',
    #     through='regiclass.Enrollment',
    #     related_name='enroll_lectures',
    # )

    # user_token = models.ManyToManyField(Token)

    objects = MyUserManager()

    def info_update(self, **kwargs):
        # self.my_photo = kwargs.get('my_photo', self.my_photo)
        self.nickname = kwargs.get('nickname', self.nickname)
        self.phone = kwargs.get('phone', self.phone)
        self.save()

    def get_user_token(self, user_pk):
        return Token.objects.get_or_create(user_id=user_pk)