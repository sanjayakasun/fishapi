from django.db import models


class FishSpecies(models.Model):
    """Model to store fish species information from the ontology"""
    scientific_name = models.CharField(max_length=200)
    vernacular_name = models.CharField(max_length=200)
    family = models.CharField(max_length=100)
    genus = models.CharField(max_length=100)
    threat_status = models.CharField(max_length=50)
    occurrence_status = models.CharField(max_length=100)
    max_size_cm = models.FloatField(null=True, blank=True)
    body_shape = models.TextField(blank=True)
    body_color = models.TextField(blank=True)
    description = models.TextField(blank=True)
    habitat_type = models.TextField(blank=True)
    water_conditions = models.TextField(blank=True)
    specific_locations = models.TextField(blank=True)
    river_basins = models.TextField(blank=True)
    districts = models.TextField(blank=True)
    protected_areas = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fish Species"
        verbose_name_plural = "Fish Species"

    def __str__(self):
        return f"{self.vernacular_name} ({self.scientific_name})"


class ChatSession(models.Model):
    """Model to store chat sessions"""
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id}"


class ChatMessage(models.Model):
    """Model to store chat messages"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
