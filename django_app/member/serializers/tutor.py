from django.contrib.auth import get_user_model
from rest_framework import serializers

from member.models import Tutor, Certification

MyUser = get_user_model()

__all__ = (
    'TutorRegisterSerializer',
    'MyUserInfoSerializer',
    'CertificationSerializer',
    'TutorSerializer'
)


class TutorRegisterSerializer(serializers.ModelSerializer):
    """ 튜터 등록 """
    my_photo = serializers.ImageField(required=True)
    nickname = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    cert_name = serializers.ListField(
        child=serializers.CharField(),
    )
    cert_photo = serializers.ListField(
        child=serializers.ImageField(),
    )

    class Meta:
        model = Tutor
        fields = (
            # TutorRegisterSerializer
            'cert_type',
            'school',
            'major',
            'status_type',

            # MyUserInfoSerializer
            'my_photo',
            'nickname',
            'phone',

            # CertificationSerializer
            'cert_name',
            'cert_photo',
        )

    def validate(self, data):
        return data


class MyUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'my_photo',
            'nickname',
            'phone',
        )


class CertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certification
        fields = (
            'cert_name',
            'cert_photo',
        )


class TutorSerializer(serializers.ModelSerializer):
    """ 튜터 정보 조회, 수정, 삭제 """
    author = MyUserInfoSerializer()
    certification = CertificationSerializer(many=True)

    class Meta:
        model = Tutor
        fields = (
            'pk',
            'cert_type',
            'school',
            'major',
            'status_type',

            'author',
            'certification',
        )

    def update(self, instance, validated_data):
        print('update')
        instance.cert_type = validated_data.get('cert_type', instance.cert_type)
        instance.school = validated_data.get('school', instance.school)
        instance.major = validated_data.get('major', instance.major)
        instance.status_type = validated_data.get('status_type', instance.status_type)

        # user = instance.author
        # user.my_photo = validated_data.get('my_photo', user.my_photo)
        # user.nickname = validated_data.get('nickname', user.nickname)
        # user.phone = validated_data.get('phone', user.phone)

        instance.save()

        return instance

    def validate(self, data):
        return data
