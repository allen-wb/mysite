from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=32)
    true_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=16)
    sex = models.SmallIntegerField()
    age = models.IntegerField()
    image = models.ImageField(upload_to='image/%Y/%m', verbose_name='文件缩略图', blank=True)
    address = models.CharField(max_length=100)
    tel = models.CharField(max_length=11)
    email = models.CharField(max_length=30)
    is_delete = models.SmallIntegerField(blank=True)
    creater = models.CharField(max_length=32)
    create_date = models.DateTimeField()
    updater = models.CharField(max_length=32, blank=True)
    update_date = models.DateTimeField(blank=True)
    remark = models.CharField(max_length=100, blank=True)


class Blog(models.Model):
    blog_id = models.CharField(primary_key=True, max_length=32)
    blog_title = models.CharField(max_length=100)
    blog_about = models.CharField(max_length=100)
    blog_content = models.TextField()
    user_id = models.CharField(max_length=32)
    is_delete = models.SmallIntegerField(blank=True)
    creater = models.CharField(max_length=32)
    create_date = models.DateTimeField()
    updater = models.CharField(max_length=32, blank=True)
    update_date = models.DateTimeField(blank=True)
    remark = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.blog_title


class Comment(models.Model):
    comment_id = models.CharField(primary_key=True, max_length=32)
    blog_id = models.CharField(max_length=32)
    comment_content = models.TextField()
    user_id = models.CharField(max_length=32)
    is_delete = models.SmallIntegerField(blank=True)
    creater = models.CharField(max_length=32)
    create_date = models.DateTimeField()
    updater = models.CharField(max_length=32, blank=True)
    update_date = models.DateTimeField(blank=True)
    remark = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.comment_content
