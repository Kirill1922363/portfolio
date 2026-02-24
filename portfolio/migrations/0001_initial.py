from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва')),
                ('category', models.CharField(choices=[('backend', 'Backend'), ('frontend', 'Frontend'), ('tools', 'Інструменти'), ('soft', 'Soft Skills')], default='backend', max_length=20, verbose_name='Категорія')),
                ('level', models.PositiveIntegerField(default=80, help_text='0–100', verbose_name='Рівень (%)')),
                ('icon', models.CharField(blank=True, help_text='Font Awesome клас, напр. fa-python', max_length=60, verbose_name='Іконка')),
            ],
            options={'verbose_name': 'Навичка', 'verbose_name_plural': 'Навички', 'ordering': ['category', '-level']},
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Назва')),
                ('description', models.TextField(verbose_name='Опис')),
                ('category', models.CharField(choices=[('django', 'Django'), ('frontend', 'Frontend'), ('python', 'Python'), ('other', 'Інше')], default='django', max_length=20, verbose_name='Категорія')),
                ('technologies', models.CharField(help_text='Через кому: Python, Django', max_length=300, verbose_name='Технології')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub')),
                ('live_url', models.URLField(blank=True, verbose_name='Живий сайт')),
                ('image', models.ImageField(blank=True, upload_to='projects/', verbose_name='Зображення')),
                ('is_featured', models.BooleanField(default=False, verbose_name='На головній')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Перегляди')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
            ],
            options={'verbose_name': 'Проєкт', 'verbose_name_plural': 'Проєкти', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ServicePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier', models.CharField(choices=[('basic', 'Базовий'), ('standard', 'Стандарт'), ('premium', 'Преміум')], max_length=20, unique=True, verbose_name='Тариф')),
                ('name', models.CharField(max_length=100, verbose_name='Назва')),
                ('price', models.DecimalField(decimal_places=0, max_digits=8, verbose_name='Ціна ($)')),
                ('description', models.TextField(verbose_name='Опис')),
                ('delivery_days', models.PositiveIntegerField(default=7, verbose_name='Термін (днів)')),
                ('revisions', models.PositiveIntegerField(default=2, verbose_name='Правок')),
                ('is_popular', models.BooleanField(default=False, verbose_name='Популярний')),
                ('color', models.CharField(default='#0D6EFD', max_length=7, verbose_name='Колір (HEX)')),
            ],
            options={'verbose_name': 'Пакет послуг', 'verbose_name_plural': 'Пакети послуг', 'ordering': ['price']},
        ),
        migrations.CreateModel(
            name='PackageFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='Функція')),
                ('is_included', models.BooleanField(default=True, verbose_name='Включена')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='portfolio.servicepackage')),
            ],
            options={'verbose_name': 'Функція пакету', 'verbose_name_plural': 'Функції пакету', 'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Назва')),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('content', models.TextField(verbose_name='Вміст')),
                ('excerpt', models.TextField(max_length=500, verbose_name='Короткий опис')),
                ('cover', models.ImageField(blank=True, upload_to='blog/', verbose_name='Обкладинка')),
                ('published', models.BooleanField(default=False, verbose_name='Опублікований')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Перегляди')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('tags', models.ManyToManyField(blank=True, to='portfolio.tag', verbose_name='Теги')),
            ],
            options={'verbose_name': 'Стаття', 'verbose_name_plural': 'Статті', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name="Ім'я")),
                ('email', models.EmailField(verbose_name='Email')),
                ('text', models.TextField(verbose_name='Коментар')),
                ('approved', models.BooleanField(default=False, verbose_name='Схвалений')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='portfolio.blogpost')),
            ],
            options={'verbose_name': 'Коментар', 'verbose_name_plural': 'Коментарі', 'ordering': ['created_at']},
        ),
        migrations.CreateModel(
            name='OrderInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name="Ім'я")),
                ('email', models.EmailField(verbose_name='Email')),
                ('project_type', models.CharField(max_length=200, verbose_name='Тип проєкту')),
                ('budget', models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True, verbose_name='Бюджет ($)')),
                ('message', models.TextField(verbose_name='Повідомлення')),
                ('status', models.CharField(choices=[('new', 'Новий'), ('in_progress', 'В роботі'), ('done', 'Виконано')], default='new', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portfolio.servicepackage', verbose_name='Пакет')),
            ],
            options={'verbose_name': 'Замовлення', 'verbose_name_plural': 'Замовлення', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=300)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={'verbose_name': 'Перегляд', 'verbose_name_plural': 'Перегляди', 'ordering': ['-created_at']},
        ),
    ]
