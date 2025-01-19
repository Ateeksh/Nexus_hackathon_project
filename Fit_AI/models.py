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
    eaten = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Excersise(models.Model):
    name = models.CharField(max_length=255)
    Reps = models.DecimalField(decimal_places=0,max_digits=2) 
    Sets =  models.DecimalField(decimal_places=2,max_digits=5) 
    Timeperrep = models.PositiveIntegerField()  
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Fitness(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255) 
    diet = models.ManyToManyField(FoodItem, related_name='diets')
    excersise = models.ManyToManyField(FoodItem, related_name='excersise')

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    weight = models.DecimalField(decimal_places=2,max_digits=5) 
    weight_goal = models.DecimalField(decimal_places=2,max_digits=5) 
    height = models.DecimalField(decimal_places=2,max_digits=5) 
    Medical_history = models.TextField()
    Additional_information = models.TextField()
    def __str__(self):
        return self.name
    
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255) 
    steps =  models.DecimalField(decimal_places=0,max_digits=5) 
    sleep = models.DecimalField(decimal_places=0,max_digits=2) 
    calories = models.DecimalField(decimal_places=0,max_digits=5) 
    weight = models.DecimalField(decimal_places=2,max_digits=5) 
    protien = models.DecimalField(decimal_places=2,max_digits=5)
    food = models.ManyToManyField(FoodItem, related_name='diets')
    Excersise_done = models.ManyToManyField(FoodItem, related_name='excersise')

    def __str__(self):
        return f"{self.user.name} - {self.date}"

class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    date = models.DateField(auto_now_add=True)  
    steps = models.DecimalField(decimal_places=0, max_digits=5) 
    sleep = models.DecimalField(decimal_places=0, max_digits=2) 
    calories = models.DecimalField(decimal_places=0, max_digits=5) 
    weight = models.DecimalField(decimal_places=2, max_digits=5) 
    protien = models.DecimalField(decimal_places=2, max_digits=5)
    
    def __str__(self):
        return f"{self.user.name} - {self.date}"