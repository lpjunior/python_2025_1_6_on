import uuid

from django.db import models

class Person(models.Model):
    #person_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    published_date = models.DateField()

    def __str__(self):
        return (f"""{{
                "title" : "{self.title}",
                "author" : "{self.author}",
                "pages" : {self.author},
                "published_date" : "{self.published_date}"
                }}""")