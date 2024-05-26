from django.db import models

class Variable(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
