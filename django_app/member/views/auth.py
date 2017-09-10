from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers.myuser import LoginSerializer


class LoginView(APIView):
    """ 일반 로그인 """

    def post(self, request, format=None):
        data = request.data.copy()
        data['user_type'] = 'd'
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            ret = serializer.validated_data
        return Response(ret)