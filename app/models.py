from django.db import models

# Create your models here.

class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=100)
    publish_date=models.DateField(null=True)

# return the human-readable presentation of each field in the Book table created above
    def __str__(self):
        return self.title
    

