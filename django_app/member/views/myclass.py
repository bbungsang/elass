from rest_framework import generics

# from member.pagination import PostPagination
from member.serializers.myclass import MyClassListSerializer, LikeClassListSerializer
from regiclass.models import Enrollment, LikeLecture

__all__ = (
    'MyClassListView',
    'LickClassListView',
)


class MyClassListView(generics.ListAPIView):
    model = Enrollment
    serializer_class = MyClassListSerializer
    # pagination_class = PostPagination

    def get_queryset(self):
        user = self.request.user
        return user.enrollment_set.all()


class LikeClassListView(generics.ListAPIView):
    model = LikeLecture
    serializer_class = LikeClassListSerializer
    # pagination_class = PostPagination

    def get_queryset(self):
        user = self.request.user
        return user.likelecture_set.all()

