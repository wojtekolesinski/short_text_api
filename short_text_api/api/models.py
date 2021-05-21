from django.db import models


class ShortText(models.Model):
    text_id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    text = models.TextField(blank=False, max_length=160)
    viewcount = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']
