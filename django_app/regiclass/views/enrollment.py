from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from regiclass.models import Lecture, Enrollment
from regiclass.serializers.enrollment import EnrollmentSerializer, LectureInfoSerializer

MyUser = get_user_model()


class EnrollmentView(APIView):
    def get(self, request, lecture_pk):
        context = {
            'user': {
                'username': request.user.username,
            }
        }
        lecture = Lecture.objects.get(pk=lecture_pk)
        serializer = LectureInfoSerializer(lecture, context=context)
        return Response(serializer.data)

    def post(self, request, lecture_pk):
        user = MyUser.objects.get(pk=request.user.pk)
        lecture = Lecture.objects.get(pk=lecture_pk)
        serializer = EnrollmentSerializer(lecture, data=request.data)
        if serializer.is_valid(raise_exception=True):
            Enrollment.objects.get_or_create(
                user=user,
                lecture=lecture,
                to_tutor=serializer.validated_data['to_tutor']
            )
            return self.get(request, lecture_pk)