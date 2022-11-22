from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    publish_date = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookProject/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False)
    user_name = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class RequestBook(models.Model):
    name = models.CharField(max_length=200)
    bookName = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)


class Review(models.Model):
    book = models.ForeignKey(Book, blank=True, null=True, on_delete=models.CASCADE)
    publishdate = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    rating = models.DecimalField(decimal_places=0, max_digits=1, default='0')

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender",on_delete=models.CASCADE, editable=False)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    subject = models.TextField(max_length=200)
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)