from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class DataType(models.Model):
    name = models.CharField(max_length=100, default='')
    capture_device = models.CharField(max_length=100, default='')
    requirements = models.CharField(max_length=100, default='')
    ns_process_data_speed = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    data_file = models.FileField(upload_to='data/')
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProcessedData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)

    STATUS_DATA_CHOICES = [
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_DATA_CHOICES)
    processed_data_file = models.FileField(upload_to='data/')

    start_date = models.DateField()
    end_date = models.DateField()
    processing_time = models.DurationField()

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.processing_time = self.end_date - self.start_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.video.name}{self.data_type}Name"

    def save_endtime(self):
        self.end_date = timezone.now()
        self.save()

class Nerf(models.Model):
    name = models.CharField(max_length=50, default='')
    long_name = models.CharField(max_length=100, default='')
    url = models.URLField(default='')
    supports_normals = models.BooleanField(default=False)
    description = models.TextField(default='')

    def __str__(self):
        return self.name

class NerfModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    processed_data = models.ForeignKey(ProcessedData, on_delete=models.CASCADE)

    model_file = models.FileField(upload_to='nerf_models/')
    nerf = models.ForeignKey(Nerf, on_delete=models.CASCADE)
    has_normals = models.BooleanField(default=False)

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
    
    def save_endtime(self):
        self.end_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.nerf.name}Model"

### NerfModel -> NerfObject

class ExportMethod(models.Model):
    name = models.CharField(max_length=50, default='')
    long_name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')

    def __str__(self):
        return self.name

class NerfObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nerf_model = models.ForeignKey(NerfModel, on_delete=models.CASCADE)
    
    object_file = models.FileField(upload_to='nerf_objects/')
    
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    export_time = models.DurationField(null=True, blank=True)

    STATUS_OBJECT_CHOICES = [
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_OBJECT_CHOICES, default='in_progress')

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.export = self.end_date - self.start_date
        super().save(*args, **kwargs)
    
    def save_endtime(self):
        self.end_date = timezone.now()
        self.save()
    
    def __str__(self):
        return f"{self.nerf_model}Object"

### Reviews

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)

    processed_data = models.ForeignKey(ProcessedData, on_delete=models.CASCADE)
    nerf_model = models.ForeignKey(NerfModel, on_delete=models.CASCADE)
    nerf_object = models.ForeignKey(NerfObject, on_delete=models.CASCADE)

    fidelity_rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)], verbose_name='Fidelity Rating')
    detail_rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)], verbose_name='Detail Rating')
    definition_rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)], verbose_name='Definition Rating')
    usability_rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)], verbose_name='Usability Rating')
    
    comment = models.TextField(blank=True)
    
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.nerf_object}"