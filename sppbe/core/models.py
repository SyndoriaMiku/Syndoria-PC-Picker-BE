from django.db import models

# Create your models here.

class Socket(models.Model):
    """Socket on CPU and Mobo"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

class RamType(models.Model):
    """RAM Type"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

class FormFactor(models.Model):
    """Form Factor"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

class CPU (models.Model):
    """CPU Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE, related_name='cpu')
    description = models.TextField(blank=True, null=True)
    
            