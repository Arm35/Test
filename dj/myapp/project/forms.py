from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.postgres.forms import SimpleArrayField
from django.forms import ModelForm
from django import forms

from. models import Test,Question,Answer

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']




# class QuestionForm(ModelForm):
#     answers = SimpleArrayField(forms.CharField(max_length=5))
#
#     class Meta:
#         model = Question
#         fields = ['question']
#
#
# class TestForm(ModelForm):
#     # questions = SimpleArrayField(forms.CharField(max_length=5))
#
#     class Meta:
#         model = Test
#         fields = ['name', 'category']




class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['name']

class QuestionForm(ModelForm):
    answers = forms.inlineformset_factory(Question, Answer, form=AnswerForm, extra=2, can_delete=True)

    class Meta:
        model = Question
        fields = ['question']

class TestForm(ModelForm):
    questions = forms.inlineformset_factory(Test, Question, form=QuestionForm, extra=2, can_delete=True)

    class Meta:
        model = Test
        fields = ['name', 'category']




class TestNameForm(ModelForm):
    class Meta:
        model = Test
        fields = ['name']


class TestCategoryForm(ModelForm):
    class Meta:
        model = Test
        fields = ['category']

class QuestionChangeForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question']

class AnswerChangeForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['name']