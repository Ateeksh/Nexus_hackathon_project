from django.db import models


class UserAccount(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255) 

    def __str__(self):
        return self.name
    
class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    protein = models.FloatField()
    usage = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Fitness(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255) 
    food_items = models.ManyToManyField(FoodItem, related_name='diets')
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    weight = models.DecimalField(decimal_places=2,max_digits=5) 
    height = models.DecimalField(decimal_places=2,max_digits=5) 
    def __str__(self):
        return self.name
    