from rest_framework import serializers

from member.models import MyUser, Tutor
from regiclass.models import Enrollment, Lecture, LikeLecture

__all__ = (
    'MyUserInfoSerializer',
    'TutorInfoSerializer',
    'LectureInfoSerializer',
    'MyClassListSerializer',
    'LikeClassListSerializer',
)


class MyUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'my_photo',
            'nickname',
        )


class TutorInfoSerializer(serializers.ModelSerializer):
    author = MyUserInfoSerializer()

    class Meta:
        model = Tutor
        fields = (
            'pk',
            'author',
        )


class LectureInfoSerializer(serializers.ModelSerializer):
    tutor = TutorInfoSerializer()

    class Meta:
        model = Lecture
        fields = (
            'title',
            'tutor',
        )


class MyClassListSerializer(serializers.ModelSerializer):
    lecture = LectureInfoSerializer()

    class Meta:
        model = Enrollment
        fields = (
            'lecture',
        )


class LikeClassListSerializer(serializers.ModelSerializer):
    lecture = LectureInfoSerializer()

    class Meta:
        model = LikeLecture
        fields = (
            'lecture',
        )