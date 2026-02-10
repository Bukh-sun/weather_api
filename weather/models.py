from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import PositiveIntegerField


class CustomerReview(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='Название продукта', help_text="Введите название продукта")
    customer_name = models.CharField(max_length=150, verbose_name='Имя', help_text="Введите имя")
    review_text = models.TextField(verbose_name='Текст отзыва', help_text="Введите текст отзыва")
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка', help_text="Выберите оценку от 1 до 5", default=5, choices=[(1, '1 Звезда'), (2, '2 Звезды'), (3, '3 Звезды'), (4, '4 Звезды'), (5, '5 Звёзд')])
    review_date = models.DateField(verbose_name='Дата отзыва', auto_now_add=True)
    is_approved = models.BooleanField(default=False, verbose_name='Отзыв подтверждён', help_text='Укажите подтверждён ли отзыв')
    likes_count = models.PositiveIntegerField(verbose_name='Количество лайков', default=0, editable=False)
    dislikes_count = models.PositiveIntegerField(verbose_name='Количество дизлайков', default=0, editable=False)
    email = models.EmailField(verbose_name='Электронная почта', help_text="Введите электронную почту")
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес клиента', null=True, editable=False)