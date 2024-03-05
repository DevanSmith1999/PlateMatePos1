from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    def _str_(self):
        return self.email
