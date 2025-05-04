from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')

    def __str__(self):
        return self.project_name

class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Member(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')

    class Meta:
        unique_together = ('member', 'project')

    def __str__(self):
        return f"{self.member.username} in {self.project.project_name}"

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    username = models.CharField(max_length=150)  # или ForeignKey к User, если надо связать
    text = models.TextField()

    def __str__(self):
        return f"Comment by {self.username} on {self.project.project_name}"