from django.contrib.auth import authenticate

from rest_framework import serializers

from member.models import Tutor, get_user_model

MyUser = get_user_model()


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