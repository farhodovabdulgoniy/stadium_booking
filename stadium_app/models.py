from django.db import models
from accounts.models import CustomUser
from django_celery_beat.models import PeriodicTask


class Stadium(models.Model):
    title = models.CharField(max_length=255)
    latitude = models.CharField(max_length=70)
    longitude = models.CharField(max_length=70)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/images/', blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='stadium')

    def __str__(self):
        return self.title
    

STATUS = (
    ('Pending', 'Pending'),
    ('Canceled', 'Canceled'),
    ('Finished', 'Finished'),
)


class Book(models.Model):
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    busy_from = models.DateTimeField()
    busy_to = models.DateTimeField()
    is_busy = models.BooleanField(default=True)
    status = models.CharField(choices=STATUS, max_length=255, default='Pending')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='book')
    
    def __str__(self) -> str:
        return f"{self.stadium} {self.busy_from} - {self.busy_to}"
    

class TaskOrder(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='task_order')
    periodic_task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.user.username
    
    