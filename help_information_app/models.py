import uuid
from django.db import models


class InformationModel(models.Model):
    """
    Model to store information for the support(information) page
    """
    publication_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
