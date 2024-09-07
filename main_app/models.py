# main_app/models.py

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


CARE_ACTIONS = (
    ('W', 'Watering'),
    ('F', 'Fertilizing'),
    ('L', 'Leaf Cleaning'),
)


class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

        # Define a method to get the URL for this particular plant instance
    def get_absolute_url(self):
        return reverse('plant-detail', kwargs={'plant_id': self.id})

class Care(models.Model):
    date = models.DateField('Care date')
    action = models.CharField(
        max_length=1,
        choices=CARE_ACTIONS,
        default=CARE_ACTIONS[0][0] 
    )
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_action_display()} on {self.date}'

    class Meta:
        ordering = ['-date']