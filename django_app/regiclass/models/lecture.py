from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

__all__ = (
    'Lecture',
    'LikeLecture',
)


class Lecture(models.Model):
    CATEGORY_HEALTHNBEAUTY = 'hbn'
    CATEGORY_LANG = 'lang'
    CATEGORY_COMPUTER = 'com'
    CATEGORY_MUSICNART = 'mna'
    CATEGORY_SPORTS = 'sports'
    CATEGORY_MAJOR = 'major'
    CATEGORY_HOBBY = 'hobby'

    CLASS_TYPE_ONETOONE = 'onetoone'
    CLASS_TYPE_GROUP = 'group'
    CLASS_TYPE_ONEDAY = 'oneday'

    STATE_EDITING = 'editing'
    STATE_ACTIVITY = 'activity'

    CATEGORY_CHOICE = (
        (CATEGORY_HEALTHNBEAUTY, '헬스&뷰티'),
        (CATEGORY_LANG, '외국어'),
        (CATEGORY_COMPUTER, '컴퓨터'),
        (CATEGORY_MUSICNART, '음악 / 미술'),
        (CATEGORY_SPORTS, '스포츠'),
        (CATEGORY_MAJOR, '전공 / 취업'),
        (CATEGORY_HOBBY, '이색취미'),
    )

    CLASS_TYPE_CHOICE = (
        (CLASS_TYPE_ONETOONE, '1:1수업'),
        (CLASS_TYPE_GROUP, '그룹수업'),
        (CLASS_TYPE_ONEDAY, '원데이')
    )

    MEMBER_COUNT = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
    )

    STATE_CHOICE = (
        (STATE_EDITING, '작성중'),
        (STATE_ACTIVITY, '활동중'),
    )

    tutor = models.ForeignKey(
        'member.Tutor',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=30,
    )
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICE,
    )
    class_type = models.CharField(
        max_length=10,
        choices=CLASS_TYPE_CHOICE,
    )
    min_member = models.CharField(
        max_length=1,
        null=True,
        choices=MEMBER_COUNT,
    )
    max_member = models.CharField(
        max_length=1,
        null=True,
        choices=MEMBER_COUNT,
    )
    cover_photo = models.ImageField(
        upload_to='class/cover/%Y/%m/%d',
    )
    tutor_intro = models.TextField()
    class_intro = models.TextField()
    target_intro = models.TextField()
    price = models.CharField(
        max_length=10,
    )
    basic_class_time = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    total_count = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    youtube_url1 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    youtube_url2 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    region_comment = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    notice = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    state = models.CharField(
        max_length=10,
        choices=STATE_CHOICE,
        default=STATE_EDITING,
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_lecture',
        through='LikeLecture',
    )
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    ##
    # 슬러그 생성
    ##
    slug = models.SlugField(
        unique=True,
        blank=True,
        db_index=True,
        allow_unicode=True,
    )

    # @permalink
    # def get_absolute_url(self):
    #     return reverse("member:detail", (), {
    #       'pk': self.pk,
    #       'slug': self.slug,
    #     })


def create_slug(instance, new_slug=None):
    slug = slugify('title-' + instance.title, allow_unicode=True)
    if new_slug is not None:
        slug = new_slug
    qs = Lecture.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Lecture)


class LikeLecture(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'lecture'),
        )