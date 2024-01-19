from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.template.backends import django
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))[
            'pcr']
        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name='Категории')
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    news = 'NE'
    article = 'AR'

    POST_TYPES = [
        (news, "Новость"),
        (article, 'Статья'),
    ]

    post_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = models.TextField()
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news, verbose_name="Вид поста")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    post_update = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name="Категория")

    def preview(self):
        return f"{self.text[:124]}..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'id-{self.pk}: {self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date_in = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
