from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=500)
    start_time = models.DateTimeField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=200, null=True)
    is_free = models.BooleanField(default=False)
    ticket_url = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['title']  # Başlığa göre alfabetik sırala

    def __str__(self):
        return f"{self.title} {self.city} {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    

