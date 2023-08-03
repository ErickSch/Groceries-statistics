from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# erick
# lionelerick54@hotmail.com
# Pass

# class Store(models.Model):
#     name = models.CharField(max_length=30)
#     location = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="images")

#     def __str__(self):
#         return self.name

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title
    



class Process(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=30)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.id






