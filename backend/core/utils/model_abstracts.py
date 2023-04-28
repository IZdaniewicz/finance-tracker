import uuid
from django.db import models


class Model(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True
