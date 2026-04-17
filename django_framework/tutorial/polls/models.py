from django.db import models

# Mọi model được biểu diễn bởi class đều là class con của Model
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200) # Mọi field đều được biểu diễn bởi instance của Field (IntegerField, ...)
    votes = models.IntegerField(default=0)
    
