from django.db import models
from App_Login.models import Teacher,Student
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


# Create your models here.

class Quiz(models.Model):
    title=models.CharField(max_length=255,null=True)
    creator=models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,related_name='quiz_teacher')
    question_count=models.IntegerField(default=0)
    quiz_created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


class Question(models.Model):
    ques_title=models.CharField(max_length=255)
    answer=models.CharField(max_length=150)
    option1=models.CharField(max_length=150)
    option2=models.CharField(max_length=150)
    option3=models.CharField(max_length=150)
    option4=models.CharField(max_length=150)
    quiz=models.ForeignKey(Quiz,related_name='question_quiz',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.ques_title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='user_answer')
    text = models.CharField(max_length=1000)
    answered_by=models.ForeignKey(Student,on_delete=models.CASCADE,null=True,related_name='student_answer')
    is_correct = models.BooleanField(default=False)
    answered= models.BooleanField(default=False)
    
    class Meta:
        unique_together = (("question", "answered_by"),)
    def __str__(self):
        return self.text+" ---- Answered By  "+self.answered_by.user.username
    
    
    
class StudentQuiz(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,null=True,related_name='student_quiz_view')
    taker=models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,related_name='student_quiz')
    attended=models.BooleanField(default=False)
    
    
    class Meta:
        unique_together = (("quiz", "taker"),)
    
        
class GradedQuiz(models.Model):
    quiz=models.OneToOneField(StudentQuiz,on_delete=models.CASCADE,null=True,related_name='student_graded_quiz')
    marks=models.IntegerField(default=0)
    graded=models.BooleanField(default=False)
    quiz_graded=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quiz.quiz.title+'.... Graded.....'+'for...'+self.quiz.taker.user.username
    
    

@receiver(post_save, sender=Question)
def set_default_quiz(sender, instance, created,**kwargs):
    quiz = Quiz.objects.filter(id = instance.quiz.id)
    quiz=quiz[0]
    if quiz:
        quiz.question_count+=1
    quiz.save()

@receiver(post_save, sender=Answer)
def set_default(sender, instance, created,**kwargs):
    if created:
        quiz = Question.objects.filter(id = instance.question.id)
        quiz=quiz[0]
        if quiz and quiz.answer==instance.text:
                instance.is_correct=True
                instance.save()