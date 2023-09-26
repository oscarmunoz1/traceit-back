from django.db import models

# Create your models here.


class Gallery(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GalleryImage(models.Model):
    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="gallery_images/")
    created_at = models.DateTimeField(auto_now_add=True)
