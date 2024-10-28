from rest_framework import serializers
from . import models
from App_Login.serializers import UserSerializer

class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Question
        fields="__all__"
        depth=1

class StudentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Question
        exclude=('answer',)
        depth=1
        
class QuizSerializer(serializers.ModelSerializer):
    question=QuestionSerializer(many=True, required=False)
    class Meta:
        model=models.Quiz
        fields="__all__"
        depth=1
        



    

class GradedQuizSerializer(serializers.ModelSerializer):
    questions=serializers.SerializerMethodField(required=False)
    class Meta:
        model=models.GradedQuiz
        fields="__all__"
        depth=1
    def get_questions(self,obj):
        question=obj.quiz.quiz.question_quiz.all()
        return QuestionSerializer(question,many=True).data 

class AnswerQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Answer
        fields="__all__"
        depth=1

class StudentAllQuizSerializer(serializers.ModelSerializer):
    quiz=QuizSerializer(many=True, required=False)
    class Meta:
        model=models.StudentQuiz
        fields="__all__"
        depth=2
