from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='书名')
    author = models.CharField(max_length=100, verbose_name='作者')
    category = models.CharField(max_length=50, verbose_name='分类')
    description = models.TextField(verbose_name='简介')
    cover_image = models.CharField(max_length=200, verbose_name='封面图片', blank=True)
    
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'
    
    def __str__(self):
        return self.title
