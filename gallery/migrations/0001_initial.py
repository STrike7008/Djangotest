# Generated by Django 5.1.7 on 2025-04-09 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='gallery/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='gallery/thumbnails/')),
            ],
        ),
        migrations.CreateModel(
            name='SliderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('image', models.ImageField(upload_to='slider/', verbose_name='Изображение')),
                ('active', models.BooleanField(default=True, verbose_name='Активно')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Изображение слайдера',
                'verbose_name_plural': 'Изображения слайдера',
                'ordering': ['order'],
            },
        ),
    ]
