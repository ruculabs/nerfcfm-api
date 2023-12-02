from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/')
    name = models.CharField(max_length=255, unique=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Nerf(models.Model):
    name = models.CharField(max_length=50, default='')
    long_name = models.CharField(max_length=100, default='')
    url = models.URLField(default='')
    description = models.TextField(default='')

    def __str__(self):
        return self.name

class ExportMethod(models.Model):
    name = models.CharField(max_length=50, default='')
    long_name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')

    def __str__(self):
        return self.name

class NerfModel(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_file = models.FileField(upload_to='nerf_models/')
    nerf = models.ForeignKey(Nerf, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    training_time = models.DurationField(null=True, blank=True)

    STATUS_MODEL_CHOICES = [
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_MODEL_CHOICES, default='in_progress')

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.training_time = self.end_date - self.start_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.video.name}{self.nerf.name}Model"

class NerfObject(models.Model):
    nerf_model = models.ForeignKey(NerfModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    object_file = models.FileField(upload_to='nerf_objects/')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    creation_time = models.DurationField(null=True, blank=True)

    STATUS_OBJECT_CHOICES = [
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_OBJECT_CHOICES, default='in_progress')

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.creation_time = self.end_date - self.start_date
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nerf_model}Object"

