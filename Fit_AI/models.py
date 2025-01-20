from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
class UserAccount(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255) 
    access =  models.DecimalField(max_digits=10, decimal_places=0,default=0)
    usage = models.BooleanField(default=True)
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
    diet = models.ManyToManyField(FoodItem, related_name='fitness_diets')  
    excersise = models.ManyToManyField(Excersise, related_name='fitness_exercises')  

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    weight = models.DecimalField(decimal_places=2,max_digits=5) 
    weight_goal = models.DecimalField(decimal_places=2,max_digits=5) 
    age= models.DecimalField(decimal_places=0,max_digits=5) 
    height = models.DecimalField(decimal_places=2,max_digits=5) 
    Medical_history = models.TextField()
    Additional_information = models.TextField()
    def __str__(self):
        return self.name

class User(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user')
    date = models.DateField()
    steps =  models.DecimalField(decimal_places=0,max_digits=5,default=0) 
    sleep = models.DecimalField(decimal_places=0,max_digits=2,default=0) 
    calories = models.DecimalField(decimal_places=0,max_digits=5,default=0) 
    weight = models.DecimalField(decimal_places=2,max_digits=5,default=0) 
    protien = models.DecimalField(decimal_places=2,max_digits=5,default=0)
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
    weight = models.DecimalField(decimal_places=2, max_digits=5,) 
    protien = models.DecimalField(decimal_places=2, max_digits=5)
    
    def __str__(self):
        return f"{self.user.name} - {self.date}"
    
@receiver(post_save, sender=User)
def sync_weight_from_user(sender, instance, **kwargs):
    if instance.weight != instance.user_profile.weight:
        instance.user_profile.weight = instance.weight
        instance.user_profile.save()

@receiver(post_save, sender=UserProfile)
def sync_weight_from_user_profile(sender, instance, **kwargs):
    user = instance.user
    if user and user.weight != instance.weight:
        user.weight = instance.weight
        user.save()