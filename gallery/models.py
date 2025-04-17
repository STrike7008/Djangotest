from django.db import models
import os
from PIL import Image
import easy_thumbnails

class GalleryImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.create_thumbnail()

    def create_thumbnail(self):
        img_path = self.image.path
        thumb_path = os.path.join(os.path.dirname(img_path), 'thumbnails', os.path.basename(img_path))
        img = Image.open(img_path)
        img.thumbnail((200, 200))
        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
        img.save(thumb_path)
        self.thumbnail = f"gallery/thumbnails/{os.path.basename(img_path)}"
        super().save(update_fields={'thumbnail'})


    def __str__(self):
        return self.title

class SliderImage(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(upload_to='slider/', verbose_name="Изображение")
    active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Изображение слайдера"
        verbose_name_plural = "Изображения слайдера"
        ordering = ['order']
