from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

# Create your models here.
class Project(models.Model):

    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Duration in months'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
        indexes = [
            models.Index(fields=['status', 'creator'])
        ]
        
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'creator'],
                name='unique_project_per_user'
            )
        ]
    
    def __str__(self):
        return self.title   
    