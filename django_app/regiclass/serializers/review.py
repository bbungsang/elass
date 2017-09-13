from rest_framework import serializers

from member.serializers import MyUserInfoSerializer
from regiclass.models import Review

# __all__ = (
#     'ReviewSerializer',
# )


class ReviewSerializer(serializers.ModelSerializer):
    author = MyUserInfoSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'curriculum_rate',
            'delivery_rate',
            'preparation_rate',
            'kindness_rate',
            'punctually_rate',
            'content',
            'modify_date',
        )
