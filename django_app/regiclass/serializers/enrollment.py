from rest_framework import serializers

from member.models import MyUser, Tutor
from regiclass.models import Enrollment, Lecture


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
    user = serializers.SerializerMethodField('get_info')

    class Meta:
        model = Lecture
        fields = (
            'title',
            'tutor',
            'user',
        )

    def get_info(self, obj):
        return self.context['user']


class EnrollmentSerializer(serializers.ModelSerializer):\

    class Meta:
        model = Enrollment
        fields = (
            'to_tutor',
        )