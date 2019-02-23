from django.db import models

# Create your models here.
class EdgeInfo(models.Model):
    address = models.CharField(max_length=32)
    balance = models.CharField(max_length=32)

class UserCheck(models.Model):
    senderAddress = models.CharField(max_length=32)
    recipientAddress = models.CharField(max_length=32)
    signature = models.CharField(max_length=32)