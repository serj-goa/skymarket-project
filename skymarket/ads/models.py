from django.conf import settings
from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    image = models.ImageField(upload_to='ads_img', null=True, blank=True, verbose_name='Картинка')
    created_at = models.DateTimeField(auto_now_add=True)

    class Mete:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created_at', )

    def __str__(self):
        return f'{self.text[:30]}...'
