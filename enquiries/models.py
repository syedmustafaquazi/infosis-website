from django.db import models

class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=120)
    company = models.CharField(max_length=160, blank=True)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=40, blank=True)
    service = models.CharField(max_length=120)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Website Enquiry'
        verbose_name_plural = 'Website Enquiries'

    def __str__(self):
        return f'{self.name} — {self.service}'
