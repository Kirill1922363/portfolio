from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend',  'Backend'),
        ('frontend', 'Frontend'),
        ('tools',    'Інструменти'),
        ('soft',     'Soft Skills'),
    ]
    name     = models.CharField(max_length=100, verbose_name='Назва')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='backend', verbose_name='Категорія')
    level    = models.PositiveIntegerField(default=80, help_text='0–100', verbose_name='Рівень (%)')
    icon     = models.CharField(max_length=60, blank=True, help_text='Font Awesome клас, напр. fa-python', verbose_name='Іконка')

    class Meta:
        verbose_name = 'Навичка'
        verbose_name_plural = 'Навички'
        ordering = ['category', '-level']

    def __str__(self):
        return f'{self.name} ({self.level}%)'


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('django',   'Django'),
        ('frontend', 'Frontend'),
        ('python',   'Python'),
        ('other',    'Інше'),
    ]
    title        = models.CharField(max_length=200, verbose_name='Назва')
    description  = models.TextField(verbose_name='Опис')
    category     = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='django', verbose_name='Категорія')
    technologies = models.CharField(max_length=300, verbose_name='Технології', help_text='Через кому: Python, Django')
    github_url   = models.URLField(blank=True, verbose_name='GitHub')
    live_url     = models.URLField(blank=True, verbose_name='Живий сайт')
    image        = models.ImageField(upload_to='projects/', blank=True, verbose_name='Зображення')
    is_featured  = models.BooleanField(default=False, verbose_name='На головній')
    views_count  = models.PositiveIntegerField(default=0, verbose_name='Перегляди')
    created_at   = models.DateTimeField(default=timezone.now, verbose_name='Дата')

    class Meta:
        verbose_name = 'Проєкт'
        verbose_name_plural = 'Проєкти'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def tech_list(self):
        return [t.strip() for t in self.technologies.split(',')]


class ServicePackage(models.Model):
    TIER_CHOICES = [
        ('basic',    'Базовий'),
        ('standard', 'Стандарт'),
        ('premium',  'Преміум'),
    ]
    tier          = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True, verbose_name='Тариф')
    name          = models.CharField(max_length=100, verbose_name='Назва')
    price         = models.DecimalField(max_digits=8, decimal_places=0, verbose_name='Ціна ($)')
    description   = models.TextField(verbose_name='Опис')
    delivery_days = models.PositiveIntegerField(default=7, verbose_name='Термін (днів)')
    revisions     = models.PositiveIntegerField(default=2, verbose_name='Правок')
    is_popular    = models.BooleanField(default=False, verbose_name='Популярний')
    color         = models.CharField(max_length=7, default='#0D6EFD', verbose_name='Колір (HEX)')

    class Meta:
        verbose_name = 'Пакет послуг'
        verbose_name_plural = 'Пакети послуг'
        ordering = ['price']

    def __str__(self):
        return f'{self.name} (${self.price})'


class PackageFeature(models.Model):
    package     = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, related_name='features')
    text        = models.CharField(max_length=200, verbose_name='Функція')
    is_included = models.BooleanField(default=True, verbose_name='Включена')
    order       = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Функція пакету'
        verbose_name_plural = 'Функції пакету'
        ordering = ['order']

    def __str__(self):
        return self.text


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Назва')
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title      = models.CharField(max_length=300, verbose_name='Заголовок')
    slug       = models.SlugField(unique=True, blank=True)
    content    = models.TextField(verbose_name='Вміст')
    excerpt    = models.TextField(max_length=500, verbose_name='Короткий опис')
    tags       = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')
    cover      = models.ImageField(upload_to='blog/', blank=True, verbose_name='Обкладинка')
    published  = models.BooleanField(default=False, verbose_name='Опублікований')
    views      = models.PositiveIntegerField(default=0, verbose_name='Перегляди')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата')

    class Meta:
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post       = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name       = models.CharField(max_length=100, verbose_name="Ім'я")
    email      = models.EmailField(verbose_name='Email')
    text       = models.TextField(verbose_name='Коментар')
    approved   = models.BooleanField(default=False, verbose_name='Схвалений')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.name} → {self.post.title}'


class OrderInquiry(models.Model):
    STATUS_CHOICES = [
        ('new',         'Новий'),
        ('in_progress', 'В роботі'),
        ('done',        'Виконано'),
    ]
    name         = models.CharField(max_length=100, verbose_name="Ім'я")
    email        = models.EmailField(verbose_name='Email')
    package      = models.ForeignKey(ServicePackage, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пакет')
    project_type = models.CharField(max_length=200, verbose_name='Тип проєкту')
    budget       = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, verbose_name='Бюджет ($)')
    message      = models.TextField(verbose_name='Повідомлення')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at   = models.DateTimeField(default=timezone.now, verbose_name='Дата')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.created_at.strftime("%d.%m.%Y")}'


class PageView(models.Model):
    path       = models.CharField(max_length=300)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Перегляд'
        verbose_name_plural = 'Перегляди'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.path} ({self.created_at.strftime("%d.%m.%Y")})'
