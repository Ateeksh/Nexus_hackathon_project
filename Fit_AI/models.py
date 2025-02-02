from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserAccount(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255) 
    access =  models.DecimalField(max_digits=10, decimal_places=0,default=0)
    usage = models.BooleanField(default=True)
    def __str__(self):
        return  f"{self.name}"

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    protein = models.FloatField()
    eaten = models.BooleanField(default=False)
    def __str__(self):
        return  f"{self.name,self.calories,self.protein}"

class Exercises(models.Model):
    name = models.CharField(max_length=255)
    Reps = models.DecimalField(decimal_places=0,max_digits=2) 
    Sets =  models.DecimalField(decimal_places=2,max_digits=5) 
    Timeperrep = models.PositiveIntegerField()  
    done = models.BooleanField(default=False)
    def __str__(self):
        return  f"{self.name,self.Reps,self.Sets,self.Timeperrep}"

class Fitness(models.Model):
    name = models.CharField(max_length=255)
    diet = models.ManyToManyField(FoodItem, related_name='fitness_diets')  
    exercise = models.ManyToManyField(Exercises, related_name='fitness_exercises')  
    def __str__(self):
        return  f"{self.name,self.diet,self.exercise}"

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    weight = models.DecimalField(decimal_places=2,max_digits=5) 
    age= models.DecimalField(decimal_places=0,max_digits=5,default=0) 
    height = models.DecimalField(decimal_places=2,max_digits=5) 
    Medical_history = models.TextField()
    Additional_information = models.TextField()
    def __str__(self):
        return f"Name: {self.name}, Weight: {self.weight}, Weight , Age: {self.age}, Height: {self.height}, Medical History: {self.Medical_history}, Additional Information: {self.Additional_information}"
    
class UserGoals(models.Model):
    name = models.CharField(max_length=255)
    steps_goal =  models.DecimalField(decimal_places=0,max_digits=5,default=10000) 
    sleep_goal = models.DecimalField(decimal_places=3,max_digits=5,default=8.00) 
    calories_goal = models.DecimalField(decimal_places=0,max_digits=5,default=2000) 
    weight_goal = models.DecimalField(decimal_places=2,max_digits=5,default=50) 
    protein_goal = models.DecimalField(decimal_places=2,max_digits=5,default=30)
    def __str__(self):
        return f"Name: {self.name}, Steps Goal: {self.steps_goal}, Sleep Goal: {self.sleep_goal}, Calories Goal: {self.calories_goal}, Weight Goal: {self.weight_goal}, Protein Goal: {self.protein_goal}"
    
class User(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    steps =  models.DecimalField(decimal_places=0,max_digits=5,default=0) 
    sleep = models.DecimalField(decimal_places=3,max_digits=5,default=0.00) 
    calories = models.DecimalField(decimal_places=0,max_digits=5,default=0) 
    weight = models.DecimalField(decimal_places=2,max_digits=5,default=0) 
    protein = models.DecimalField(decimal_places=2,max_digits=5,default=0)
    food = models.ManyToManyField(FoodItem, related_name='diets')
    Excersise_done = models.ManyToManyField(FoodItem, related_name='excersise')
    def __str__(self):
        return f"Name: {self.name}, Date: {self.date}, Steps: {self.steps}, Sleep: {self.sleep}, Calories: {self.calories}, Weight: {self.weight}, Protein: {self.protein}, Food: {self.food}, exercise Done: {self.Excersise_done}"


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    date = models.DateField(auto_now_add=True)  
    steps = models.DecimalField(decimal_places=0, max_digits=5) 
    sleep = models.DecimalField(decimal_places=3,max_digits=5,default=0.00) 
    calories = models.DecimalField(decimal_places=0, max_digits=5) 
    weight = models.DecimalField(decimal_places=2, max_digits=5,) 
    protein = models.DecimalField(decimal_places=2, max_digits=5)
    food = models.ManyToManyField(FoodItem, related_name='historydiets')
    Excersise_done = models.ManyToManyField(FoodItem, related_name='historyexcersise')
    def __str__(self):
            return  f"{self.user,self.date,self.steps,self.sleep,self.calories,self.weight,self.protein,self.food,self.Excersise_done}"

