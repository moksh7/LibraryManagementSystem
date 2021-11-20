from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
class Book(models.Model):
    '''Store information about a book'''
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    availability = models.IntegerField()
    def __str__(self):
        return self.name

class LibraryAdmin(models.Model):
    '''Extending CustomUser model to perform CRUD operations on Book model'''

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class Student(models.Model):
    ''' Extending CustomUser model. This model is be used to add relation with Book model and store information regarding books issued by student. '''

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    books_issued = models.ManyToManyField(Book,through="Record")

    def __str__(self):
        return self.user.email

class Record(models.Model):
    '''Intermediate model to store info about transaction that takes place when student issues a book'''

    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    date_issued = models.DateField(default=timezone.now)
