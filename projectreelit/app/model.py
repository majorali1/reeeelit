from django.db import models

from datetime import *
# Create your models here.

#Simple user model with Interger only password and no hashing for now


def get_currenttime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")




class User(models.Model):
    name = models.CharField(max_length=22,null=False,unique=True)
    email = models.EmailField(unique=True,max_length=60)
    password = models.IntegerField()

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=65,null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(default=get_currenttime)
    created_by = models.ForeignKey(User, related_name="user",on_delete=models.CASCADE)
    comments_num = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments',on_delete=models.CASCADE)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(default=get_currenttime)

    def __str__(self):
        return f' {self.user.name} on {self.post.title}'

class Like_dislike(models.Model):
    user = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='post',on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user','post')