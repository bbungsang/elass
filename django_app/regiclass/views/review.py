from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from regiclass.models import Lecture, Review
from regiclass.serializers import ReviewSerializer

MyUser = get_user_model()

__all__ = (
    'Reviews',
)


class Reviews(APIView):
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = MyUser.objects.get(pk=request.user.id)
            lecture = Lecture.objects.get(pk=request.data['lecture_id'])
            serializer.save(author=user, lecture=lecture)
            return Response({'result': status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        review_list = Review.objects.filter().order_by('-modify_date')[:4]
        serializer = self.serializer_class(review_list, many=True)
        return Response(serializer.data)
