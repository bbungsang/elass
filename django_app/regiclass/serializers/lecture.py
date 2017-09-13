from django.db.models import Sum, Avg
from rest_framework import serializers

from regiclass.models import Lecture, ClassLocation, LecturePhoto, Curriculum
from regiclass.serializers import ReviewSerializer
from utils.custom_exceptions import CustomIndexError, custom_index_error

# __all__ = (
#     'ClassLocationSerializer',
#     'LecturePhotoSerializer',
#     'CurriculumSerializer',
#     'LectureListSerializer',
#     'LectureMakeSerializer',
#     'LectureUpdateSerializer',
# )


class ClassLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLocation
        fields = (
            'id',
            'location1',
            'location2',
            'location_option',
            'location_detail',
            'location_etc_type',
            'location_etc_text',
            'class_weekday',
            'class_time',
        )


class LecturePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturePhoto
        fields = (
            'id',
            'lecture_photo',
        )


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = (
            'id',
            'curriculum_photo',
            'curriculum_desc',
        )


class LectureListSerializer(serializers.ModelSerializer):
    locations = ClassLocationSerializer(many=True, read_only=True)
    lecture_photos = LecturePhotoSerializer(many=True, read_only=True)
    curriculum = CurriculumSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = (
            'id',
            'tutor',
            'title',
            'category',
            'class_type',
            'min_member',
            'max_member',
            'cover_photo',
            'tutor_intro',
            'class_intro',
            'target_intro',
            'price',
            'basic_class_time',
            'total_count',
            'youtube_url1',
            'youtube_url2',
            'region_comment',
            'notice',
            'like_users',
            'state',
            'modify_date',

            'locations',
            'lecture_photos',
            'curriculum',
            'reviews',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = self.context['user']
        if user.is_authenticated:
            ret['is_like'] = instance.likelecture_set.filter(user=user, lecture=instance.id).exists()
        ret['like_count'] = instance.likelecture_set.count()
        ret['review_count'] = instance.reviews.count()
        ret['review_average'] = instance.reviews.filter(lecture=instance.id).aggregate(
            curriculum_rate=Avg('curriculum_rate'),
            delivery_rate=Avg('delivery_rate'),
            preparation_rate=Avg('preparation_rate'),
            kindness_rate=Avg('kindness_rate'),
            punctually_rate=Avg('punctually_rate')
        )
        ret['review_sum'] = instance.reviews.filter(lecture=instance.id).aggregate(
            curriculum_rate=Sum('curriculum_rate'),
            delivery_rate=Sum('delivery_rate'),
            preparation_rate=Sum('preparation_rate'),
            kindness_rate=Sum('kindness_rate'),
            punctually_rate=Sum('punctually_rate')
        )
        ret['tutor_info'] = {
            'nickname': instance.tutor.author.nickname,
        }
        return ret


class LectureMakeSerializer(serializers.ModelSerializer):
    location1 = serializers.ListField(
        child=serializers.CharField(),
    )
    location2 = serializers.ListField(
        child=serializers.CharField(),
    )
    location_option = serializers.ListField(
        child=serializers.CharField(),
    )
    location_detail = serializers.ListField(
        child=serializers.CharField(),
    )
    location_etc_type = serializers.ListField(
        child=serializers.CharField(),
    )
    location_etc_text = serializers.ListField(
        child=serializers.CharField(),
    )
    class_weekday = serializers.ListField(
        child=serializers.CharField(),
    )
    class_time = serializers.ListField(
        child=serializers.CharField(),
    )
    lecture_photo = serializers.ListField(
        child=serializers.ImageField(),
    )
    curriculum_photo = serializers.ListField(
        child=serializers.ImageField(),
    )
    curriculum_desc = serializers.ListField(
        child=serializers.CharField(),
    )

    def save(self, tutor, **kwargs):
        lecture, lecture_created = Lecture.objects.get_or_create(
            tutor=tutor,
            title=self.validated_data.get('title', ''),
            category=self.validated_data.get('category', ''),
            class_type=self.validated_data.get('class_type', ''),
            min_member=self.validated_data.get('min_member', ''),
            max_member=self.validated_data.get('max_member', ''),
            cover_photo=self.validated_data.get('cover_photo', ''),
            tutor_intro=self.validated_data.get('tutor_intro', ''),
            class_intro=self.validated_data.get('class_intro', ''),
            target_intro=self.validated_data.get('target_intro', ''),
            price=self.validated_data.get('price', ''),
            basic_class_time=self.validated_data.get('basic_class_time', ''),
            total_count=self.validated_data.get('total_count', ''),
            youtube_url1=self.validated_data.get('youtube_url1', ''),
            youtube_url2=self.validated_data.get('youtube_url2', ''),
            region_comment=self.validated_data.get('region_comment', ''),
            notice=self.validated_data.get('notice', ''),
        )

        if lecture_created:
            status = True
            message = ''
            try:
                location_len = len(self.validated_data['location1'])
                for i in range(location_len):
                    ClassLocation.objects.get_or_create(
                        lecture=lecture,
                        location1=custom_index_error(self.validated_data, 'location1', location_len)[i],
                        location2=custom_index_error(self.validated_data, 'location2', location_len)[i],
                        location_option=custom_index_error(self.validated_data, 'location_option', location_len)[i],
                        location_detail=custom_index_error(self.validated_data, 'location_detail', location_len)[i],
                        location_etc_type=custom_index_error(self.validated_data, 'location_etc_type', location_len)[i],
                        location_etc_text=custom_index_error(self.validated_data, 'location_etc_text', location_len)[i],
                        class_weekday=custom_index_error(self.validated_data, 'class_weekday', location_len)[i],
                        class_time=custom_index_error(self.validated_data, 'class_time', location_len)[i],
                    )

                lecture_photo_len = len(self.validated_data['lecture_photo'])
                for j in range(lecture_photo_len):
                    LecturePhoto.objects.get_or_create(
                        lecture=lecture,
                        lecture_photo=custom_index_error(self.validated_data, 'lecture_photo', lecture_photo_len)[j],
                    )

                curriculum_photo_len = len(self.validated_data['curriculum_photo'])
                for k in range(curriculum_photo_len):
                    Curriculum.objects.get_or_create(
                        lecture=lecture,
                        curriculum_photo=custom_index_error(self.validated_data, 'curriculum_photo', curriculum_photo_len)[k],
                        curriculum_desc=custom_index_error(self.validated_data, 'curriculum_desc', curriculum_photo_len)[k]
                    )
            except CustomIndexError as e:
                lecture.delete()
                status = False
                message = e

        return {'status': status, 'message': message}

    class Meta:
        model = Lecture
        fields = (
            'title',
            'category',
            'class_type',
            'min_member',
            'max_member',
            'cover_photo',
            'tutor_intro',
            'class_intro',
            'target_intro',
            'price',
            'basic_class_time',
            'total_count',
            'youtube_url1',
            'youtube_url2',
            'region_comment',
            'notice',

            'location1',
            'location2',
            'location_option',
            'location_detail',
            'location_etc_type',
            'location_etc_text',
            'class_weekday',
            'class_time',

            'lecture_photo',

            'curriculum_photo',
            'curriculum_desc',
        )
        read_only_fields = (
            'lecture',
        )


class LectureUpdateSerializer(serializers.ModelSerializer):
    location1 = serializers.ListField(
        child=serializers.CharField(),
    )
    location2 = serializers.ListField(
        child=serializers.CharField(),
    )
    location_option = serializers.ListField(
        child=serializers.CharField(),
    )
    location_detail = serializers.ListField(
        child=serializers.CharField(),
    )
    location_etc_type = serializers.ListField(
        child=serializers.CharField(),
    )
    location_etc_text = serializers.ListField(
        child=serializers.CharField(),
    )
    class_weekday = serializers.ListField(
        child=serializers.CharField(),
    )
    class_time = serializers.ListField(
        child=serializers.CharField(),
    )
    lecture_photo = serializers.ListField(
        child=serializers.ImageField(),
    )
    curriculum_photo = serializers.ListField(
        child=serializers.ImageField(),
    )
    curriculum_desc = serializers.ListField(
        child=serializers.CharField(),
    )

    def save(self, tutor, lecture, **kwargs):

        lecture.title = self.validated_data.get('title', '')
        lecture.category = self.validated_data.get('category', '')
        lecture.class_type = self.validated_data.get('class_type', '')
        lecture.min_member = self.validated_data.get('min_member', '')
        lecture.max_member = self.validated_data.get('max_member', '')
        lecture.cover_photo = self.validated_data.get('cover_photo', '')
        lecture.tutor_intro = self.validated_data.get('tutor_intro', '')
        lecture.class_intro = self.validated_data.get('class_intro', '')
        lecture.target_intro = self.validated_data.get('target_intro', '')
        lecture.price = self.validated_data.get('price', '')
        lecture.basic_class_time = self.validated_data.get('basic_class_time', '')
        lecture.total_count = self.validated_data.get('total_count', '')
        lecture.youtube_url1 = self.validated_data.get('youtube_url1', '')
        lecture.youtube_url2 = self.validated_data.get('youtube_url2', '')
        lecture.region_comment = self.validated_data.get('region_comment', '')
        lecture.notice = self.validated_data.get('notice', '')
        lecture.save()

        lecture.locations.all().delete()
        for i in range(len(self.validated_data['location1'])):
            ClassLocation.objects.get_or_create(
                lecture=lecture,
                location1=self.validated_data['location1'][i],
                location2=self.validated_data['location2'][i],
                location_option=self.validated_data['location_option'][i],
                location_detail=self.validated_data['location_detail'][i],
                location_etc_type=self.validated_data['location_etc_type'][i],
                location_etc_text=self.validated_data['location_etc_text'][i],
                class_weekday=self.validated_data['class_weekday'][i],
                class_time=self.validated_data['class_time'][i],
            )

        lecture.lecture_photos.all().delete()
        for j in range(len(self.validated_data['lecture_photo'])):
            LecturePhoto.objects.get_or_create(
                lecture=lecture,
                lecture_photo=self.validated_data['lecture_photo'][j],
            )

        lecture.curriculum.all().delete()
        for k in range(len(self.validated_data['curriculum_photo'])):
            Curriculum.objects.get_or_create(
                lecture=lecture,
                curriculum_photo=self.validated_data['curriculum_photo'][k],
                curriculum_desc=self.validated_data['curriculum_desc'][k]
            )

    class Meta:
        model = Lecture
        fields = (
            'title',
            'category',
            'class_type',
            'min_member',
            'max_member',
            'cover_photo',
            'tutor_intro',
            'class_intro',
            'target_intro',
            'price',
            'basic_class_time',
            'total_count',
            'youtube_url1',
            'youtube_url2',
            'region_comment',
            'notice',

            'location1',
            'location2',
            'location_option',
            'location_detail',
            'location_etc_type',
            'location_etc_text',
            'class_weekday',
            'class_time',

            'lecture_photo',

            'curriculum_photo',
            'curriculum_desc',
        )
        read_only_fields = (
            'lecture',
        )