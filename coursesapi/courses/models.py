from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    pass


class Category(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Course(BaseModel):
    subject = models.CharField(max_length=100)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='courses/%Y/%m/')

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.subject


class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='lessons/%Y/%m/')

    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', blank=True, related_name='lessons')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.subject


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Interaction(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


class Like(Interaction):
    class Meta:
        unique_together = ('user', 'lesson')