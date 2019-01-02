import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
# 多表继承
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    food = models.CharField(max_length=50)
    pizza = models.BooleanField(default=False)

    # 代理
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class MyPerson(Person):
    class Meta:
        proxy = True
        ordering = ["last_name"]

    def do_something(self):
        pass
# 多重继承
class Article(models.Model):
    article_id = models.AutoField(primary_key=True) #自定义id
    art_name= models.CharField(max_length=30)

class Book(models.Model):
    book_id = models.AutoField(primary_key=True) #自定义id
    book_name = models.CharField(max_length=30)

class BookReview(Book, Article):
    review_name=models.CharField(max_length=30,help_text='review_name帮助信息',null=True,blank=True)
    dur_data=models.DurationField(blank=True)
    filePathField_case=models.FilePathField(blank=True,path=r'd:/')
    fileField_case=models.FileField(blank=True)
    # ImageField_case=models.ImageField(blank=True)
    TimeField_case=models.TimeField(blank=True)
    ForeignKey_case=models.ForeignKey('self',on_delete=models.CASCADE,blank=True)
    def __str__(self):
        return self.review_name
# query set test
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline