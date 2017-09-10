from django.contrib.auth import authenticate

from rest_framework import serializers

from member.models import Tutor, get_user_model

MyUser = get_user_model()


class MyUserSerializer(serializers.ModelSerializer):
    """ 회원가입, 마이페이지 조회/수정/삭제 """

    password = serializers.CharField(label='Password', write_only=True)
    confirm_password = serializers.CharField(label='Confirm Password', write_only=True)

    class Meta:
        model = MyUser
        fields = (
            'username',
            'password',
            'confirm_password',
            'name',
            'nickname',
            'email',
            'phone',
            'my_photo',
        )

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # 모델 시리얼라이즈이므로 불필요한 사항?
        instance.name = validated_data.get('name', instance.name)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.my_photo = validated_data.get('my_photo', instance.my_photo)

        # password = validated_data.get('password', None)
        # instance.set_password(password)

        instance.save()
        return instance

    def validate(self, data):
        if data['password'] and data['password'] != data['confirm_password']:
            raise serializers.ValidationError('비밀번호가 서로 일치하지 않습니다.')

        # 데이터베이스에 있는 필드가 아니므로 제외
        data.pop('confirm_password')
        return data


class LoginSerializer(serializers.Serializer):
    """ 로그인 """
    username = serializers.CharField(max_length=36, write_only=True)
    password = serializers.CharField(max_length=64, write_only=True)
    user_type = serializers.CharField(max_length=1, )

    def validate(self, data):
        username = data['username']
        # user = settings.AUTH_USER_MODEL.objects.get(username=username)
        user = MyUser.objects.get(username=username)

        try:
            tutor = Tutor.objects.get(author=user)
            tutor_pk = tutor.pk
        except Tutor.DoesNotExist:
            tutor_pk = None

        if data['user_type'] == 'd':
            password = data['password']

            auth = authenticate(username=username, password=password)
            if auth is None:
                raise serializers.ValidationError({"detail": "Password is not matched"})

        token, created = user.get_user_token(user.pk)

        ret = {
            'token': token.key,
            'user': {
                'user_pk': user.pk,
                'tutor_pk': tutor_pk,
                'username': username,
                'nickname': user.nickname,
            }
        }
        return ret