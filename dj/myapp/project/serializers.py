from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from . models import Category,Test,Question,Answer,TestRating

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields = '__all__'









class AnswerSerializer(ModelSerializer):
    class Meta:
        model= Answer
        fields = '__all__'

class QuestionSerializer(ModelSerializer):
    answers=AnswerSerializer(many=True)

    class Meta:
        model=Question
        fields = '__all__'


class TestSerializer(ModelSerializer):
    questions=QuestionSerializer(many=True)
    category=CategorySerializer()
    class Meta:
        model=Test
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    test=TestSerializer()
    user=UserSerializer()
    class Meta:
        model=TestRating
        fields = '__all__'