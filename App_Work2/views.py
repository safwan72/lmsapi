from django.shortcuts import render
from . import models,serializers
from App_Login.models import Teacher,Student
from rest_framework import viewsets,generics,mixins,response
# Create your views here.



class StudentQuestionSerializerView(generics.RetrieveAPIView):
    queryset=models.Question.objects.all()
    serializer_class=serializers.StudentQuestionSerializer
    lookup_field='pk'
    def retrieve(self,*args,**kwargs):
        questions=models.Question.objects.filter(quiz=kwargs['pk'])
        serializer=serializers.StudentQuestionSerializer(questions,many=True)
        return response.Response(serializer.data)

class QuestionSerializerView(viewsets.ModelViewSet):
    queryset=models.Question.objects.all()
    serializer_class=serializers.QuestionSerializer
    lookup_field='quiz'
    def retrieve(self,*args,**kwargs):
        questions=models.Question.objects.filter(quiz=kwargs['quiz'])
        serializer=serializers.QuestionSerializer(questions,many=True)
        return response.Response(serializer.data)
    
    def create(self,request,*args,**kwargs):
        quiz=request.data['quiz']
        quizs=models.Quiz.objects.get(id=quiz)
        question=models.Question.objects.create(
            ques_title=request.data['question'],
            answer=request.data['answer'],
            option1=request.data['option1'],
            option2=request.data['option2'],
            option3=request.data['option3'],
            option4=request.data['option4'],
            quiz=quizs
        )
        questionserializer=serializers.QuestionSerializer(question)
        return response.Response(questionserializer.data)

class QuizIndividualView(generics.ListAPIView):
    queryset=models.Quiz.objects.all()
    serializer_class=serializers.QuizSerializer
    lookup_field='id'
    def get_queryset(self):
        return models.Quiz.objects.filter(id=self.kwargs['id'])




class QuizSerializerView(viewsets.ModelViewSet):
    queryset=models.Quiz.objects.all()
    serializer_class=serializers.QuizSerializer
    lookup_field='creator__user'
    def retrieve(self,*args,**kwargs):
        quiz=models.Quiz.objects.filter(creator__user=kwargs['creator__user'])
        serializer=serializers.QuizSerializer(quiz,many=True)
        return response.Response(serializer.data)
    
    def create(self,request,*args,**kwargs):
        user=request.data['creator']
        creator=Teacher.objects.get(user=user)
        title=request.data['title']
        quiz=models.Quiz.objects.create(
            creator=creator,
            title=title
        )
        quizserializer=serializers.QuizSerializer(quiz)
        return response.Response(quizserializer.data)
    
    
class GradedQuizView(viewsets.ModelViewSet):
    queryset=models.GradedQuiz.objects.all()
    serializer_class=serializers.GradedQuizSerializer
    lookup_field='quiz__taker__user'
    def retrieve(self,*args,**kwargs):
        quiz=models.GradedQuiz.objects.filter(quiz__taker__user=kwargs['quiz__taker__user'],graded=True)
        serializer=serializers.GradedQuizSerializer(quiz,many=True)
        return response.Response(serializer.data)    

    def create(self, request, *args, **kwargs):
        quiz=models.Quiz.objects.get(id=request.data['quiz'])
        student=Student.objects.get(user=request.data['taken_by'])
        question=models.Question.objects.filter(quiz=quiz)
        student_quiz=models.StudentQuiz.objects.create(quiz=quiz,taker=student)
        correct=[]
        if question.exists():
            for item in question:
                answers=models.Answer.objects.filter(question=item,is_correct=True,answered_by=student)
                if answers:
                    answersy=answers[0]
                    correct.append(answersy)
        corrects=len(correct)
        student_quiz.attended=True
        student_quiz.save()
        answer=models.GradedQuiz.objects.create(quiz=student_quiz)
        answer.marks=corrects*20
        answer.graded=True
        answer.save()
        serializer=serializers.GradedQuizSerializer(answer)
        return response.Response(serializer.data)

    


class StudentAllQuizSerializerView(viewsets.ModelViewSet):
    queryset=models.StudentQuiz.objects.all()
    serializer_class=serializers.StudentAllQuizSerializer
    lookup_field='taker__user'
    def retrieve(self,*args,**kwargs):
        quiz=models.StudentQuiz.objects.filter(taker__user=kwargs['taker__user'],attended=False)
        if quiz:
            serializer=serializers.StudentAllQuizSerializer(quiz,many=True)
        else:
            quiz=models.Quiz.objects.all()
            serializer=serializers.StudentAllQuizSerializer(quiz,many=True)
        return response.Response(serializer.data)    


class AnswerView(viewsets.ModelViewSet):
    queryset=models.Answer.objects.all()
    serializer_class=serializers.AnswerQuizSerializer
    def create(self, request, *args, **kwargs):
        question=models.Question.objects.get(id=request.data['question'])
        student=Student.objects.get(user=request.data['answered_by'])
        answer=models.Answer.objects.create(text=request.data['text'],question=question,answered_by=student,answered=True)
        serializer=serializers.AnswerQuizSerializer(answer)
        return response.Response(serializer.data)
