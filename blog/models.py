from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Post(models.Model):
    serial_no = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, default='')
    content = models.TextField()
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + ' ' +  'by' + ' ' + self.author

class BlogComment(models.Model):
    serial_number = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..."
    