from django.db import models

# Create your models here.

class Word(models.Model):
    difficulty = models.IntegerField()
    word       = models.CharField(max_length=50)

    def __str__(self):
        return self.word + " - " + str(self.difficulty)

    class Meta:
        db_table = 'PML_word'

