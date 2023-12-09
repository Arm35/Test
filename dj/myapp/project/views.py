from django.shortcuts import render
from .forms import UserForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, viewsets
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .serializers import UserSerializer, CategorySerializer,TestSerializer,RatingSerializer
from .models import Category, Answer,Question,Test,TestRating
from .forms import TestForm,QuestionForm, AnswerForm,TestNameForm,QuestionChangeForm,AnswerChangeForm,TestCategoryForm
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, parser_classes

from django.core.mail import send_mail
from django.conf import settings


@api_view(["POST"])
def register(request):
    if request.method == "POST":
        form = UserForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'data added'})
        else:
            return Response({'errors': form.errors})


@api_view(["POST"])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide username and password'})
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'})

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({'message': 'logout successfully'})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({'user': UserSerializer(request.user).data})


@api_view(["GET"])
def getCategory(request):
    data = Category.objects.all()
    return Response({'category':
                         CategorySerializer(data, many=True).data})


# @api_view(["POST"])
# # @permission_classes([IsAuthenticated])
# def add_test(request):
#     print(request.data)
#     if request.method == 'POST':
#         test_form = TestForm(request.data)
#
#         options_data = request.data.get('options', [])
#
#         if test_form.is_valid():
#             test = test_form.save()
#             for answer_text in options_data:
#                 Answer.objects.create(answer=answer_text, question=test)
#
#             return Response({'message': 'data added'})
#         else:
#             errors = {
#                 'test_form_errors': test_form.errors,
#             }
#             return Response({'errors': errors})
#     else:
#         return Response({'errors': 'Invalid method'})



# @api_view(["POST"])
# def add_test(request):
#     if request.method == 'POST':
#         test_form = TestForm(request.data)
#         if test_form.is_valid():
#             test = test_form.save()
#
#             questions_data = request.data.get('questions', [])
#             for question_data in questions_data:
#                 question_form = QuestionForm(question_data)
#                 if question_form.is_valid():
#                     question = question_form.save(commit=False)
#                     question.test = test
#                     question.save()
#
#                     answers_data = question_data.get('answers', [])
#                     for answer_data in answers_data:
#                         answer_form = AnswerForm(data=answer_data)
#                         if answer_form.is_valid():
#                             answer = answer_form.save(commit=False)
#                             answer.question = question
#                             answer.save()
#
#                             if answer_data.get('status') :
#                                 answer.status = not answer.status
#                                 answer.save()
#                         else:
#                             errors = {
#                                 'answer_form_errors': answer_form.errors,
#                             }
#                             return Response({'errors': errors})
#                 else:
#                     errors = {
#                         'question_form_errors': question_form.errors,
#                     }
#                     return Response({'errors': errors})
#
#             return Response({'message': 'Data added successfully'})
#         else:
#             errors = {
#                 'test_form_errors': test_form.errors,
#             }
#             return Response({'errors': errors})
#     else:
#         return Response({'errors': 'Invalid method'})




@api_view(["POST"])
def add_test(request):
    if request.method == 'POST':
        test_form = TestForm(request.data)
        if test_form.is_valid():
            test = test_form.save()

            questions_data = request.data.get('questions', [])
            for question_data in questions_data:
                question_form = QuestionForm(question_data)
                if question_form.is_valid():
                    question = question_form.save(commit=False)
                    question.test = test
                    question.save()

                    answers_data = question_data.get('answers', [])
                    for answer_data in answers_data:
                        answer_form = AnswerForm(data=answer_data)
                        if answer_form.is_valid():
                            answer = answer_form.save(commit=False)
                            answer.question = question
                            answer.save()

                            if answer_data.get('status'):
                                answer.status = not answer.status
                                answer.save()
                        else:
                            errors = {
                                'answer_form_errors': answer_form.errors,
                            }
                            return Response({'errors': errors})
                else:
                    errors = {
                        'question_form_errors': question_form.errors,
                    }
                    return Response({'errors': errors})



            subject = 'New Test Added'
            message = 'A new test was added!'
            from_email = 'babayanarman9627@gmail.com'
            users = User.objects.all()
            recipient_list = [user.email for user in users]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)


            return Response({'message': 'Data added successfully'})
        else:
            errors = {
                'test_form_errors': test_form.errors,
            }
            return Response({'errors': errors})
    else:
        return Response({'errors': 'Invalid method'})





# @api_view(["POST"])
# def add_test(request):
#     test_form = TestForm(request.data)
#     if test_form.is_valid():
#         test_instance = test_form.save()
#
#         for question_data in request.data.get("questions", []):
#             question_form = QuestionForm(question_data)
#             if question_form.is_valid():
#                 question_instance = question_form.save()
#                 test_instance.questions.add(question_instance)
#             else:
#                 return Response(
#                     {"error": "error data"},
#                 )
#         return Response({"success": "Test added successfully"})
#     else:
#         return Response(test_form.errors)





# @api_view(["POST"])
# def add_test(request):
#     if request.method == 'POST':
#         form = TestForm(request.data, prefix='test')
#         if form.is_valid():
#             form.save()
#             return Response({"message": "Test added successfully"})
#         else:
#             return Response({"error": "error data", "errors": form.errors})
#     else:
#         form = TestForm(prefix='test')
#
#     return Response({"error": "error request method"})


# @api_view(["POST"])
# def add_test(request):
#     if request.method == 'POST':
#         form = TestForm(request.POST, prefix='test')
#         if form.is_valid():
#             form.save()
#             return Response({"message": "Test added successfully"})
#     else:
#         form = TestForm(prefix='test')
#
#     return Response({"error": "error data"})


@api_view(["PUT"])
def set_ture(request, id):
    answer = Answer.objects.get(pk=id)
    answer.status = not answer.status
    answer.save()
    return Response({"message": "successfully"})


@api_view(["GET"])
def get_answer_id(request, id):
    answer = get_object_or_404(Answer, pk=id)

    return Response({'correctAnswerId': answer.id})


@api_view(["GET"])
def get_test(request):
    data = Test.objects.all()
    return Response({'test':
                         TestSerializer(data, many=True).data})

@api_view(["GET"])
def test_page(request, id):
    data = Test.objects.get(pk=id)
    return Response({'page': TestSerializer(data).data})


@api_view(["DELETE"])
def delete_test(request, id):
    try:
        test = Test.objects.get(pk=id)
        test.delete()
        return Response({'message': 'Test deleted'})
    except Test.DoesNotExist:
        return Response({'errors': 'Test not found'})


@api_view(["POST"])
def set_archive(request, id):
    test = Test.objects.get(pk=id)
    test.archive = not test.archive
    test.save()
    return Response({"message": "successfully"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])

def add_rating(request):
    test_id = request.data.get('testId')
    rating = request.data.get('rating')

    if test_id is None or rating is None:
        return Response({'error': ' ID and rating are required fields'})

    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return Response({'error': 'Test not found'})

    user = request.user

    if TestRating.objects.filter(user=user, test=test).exists():
        return Response({'error': 'You have already passed this test'},
                        )

    test_rating = TestRating(user=user, test=test, rating=rating)
    test_rating.save()

    return Response({'message': 'Rating added successfully'})


@api_view(["GET"])
def user_rating(request):
    data = TestRating.objects.filter(user=request.user)
    serializer = RatingSerializer(data, many=True)
    return Response({'rating': serializer.data})


@api_view(["GET"])
def all_ratings(request):
    data = TestRating.objects.all()
    serializer = RatingSerializer(data, many=True)
    return Response({'rating': serializer.data})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_test_data(request, test_id):
    try:
        test = Test.objects.get(pk=test_id)
    except Test.DoesNotExist:
        return Response({"error": "Test not found"})

    if request.method == "PUT":
        test_form = TestForm(request.data, instance=test)
        if test_form.is_valid():
            test_form.save()

            questions_data = request.data.get('questions')
            if questions_data:
                for question_data in questions_data:
                    question_id = question_data.get('id')
                    try:
                        question = Question.objects.get(pk=question_id, test=test)
                    except Question.DoesNotExist:
                        continue

                    answers_data = question_data.get('answers')
                    if answers_data:
                        for answer_data in answers_data:
                            answer_id = answer_data.get('id')
                            try:
                                answer = Answer.objects.get(pk=answer_id, question=question)
                            except Answer.DoesNotExist:
                                continue

                            answer_form = AnswerForm(answer_data, instance=answer)
                            if answer_form.is_valid():
                                answer_form.save()

            return Response({"success": "Test data updated successfully"})
        else:
            return Response({"error": "Invalid data"})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def change_test_name(request, test_id):
    test = Test.objects.get(id=test_id)

    if request.method == 'PUT':
        form = TestNameForm(data=request.data, instance=test)

        if form.is_valid():
            form.save()
            return Response({"message": "Test name updated successfully."})
        else:
            return Response({"error": form.errors})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def change_quastion(request, question_id):
    question = Question.objects.get(id=question_id)

    if request.method == 'PUT':
        form = QuestionChangeForm(data=request.data, instance=question)

        if form.is_valid():
            form.save()
            return Response({"message": "Question updated successfully."})
        else:
            return Response({"error": form.errors})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def change_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)

    if request.method == 'PUT':
        form = AnswerChangeForm(data=request.data, instance=answer)

        if form.is_valid():
            form.save()
            return Response({"message": "Question updated successfully."})
        else:
            return Response({"error": form.errors})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def change_category(request, test_id):
    test = Test.objects.get(id=test_id)

    if request.method == 'PUT':
        form = TestCategoryForm(data=request.data, instance=test)

        if form.is_valid():
            form.save()
            return Response({"message": "Question updated successfully."})
        else:
            return Response({"error": form.errors})


