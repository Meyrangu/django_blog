from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    area_ch = [
        ('SOUTH', 'South'),
        ('NORTH', 'North'),
        ('CENTER', 'Center'),
    ]
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)
    thumb = models.ImageField(default='default.jpg', blank=True)
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    area = models.TextField(max_length=10, choices=area_ch)
    howto = models.TextField(default='')
    len1 = models.IntegerField(default=1)
    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_on']
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)