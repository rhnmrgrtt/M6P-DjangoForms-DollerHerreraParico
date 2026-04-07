'''
Rhinakels Herrera, 245785; Zale Sebastian Latonio, 242494 ; Nathan Riley Sy, 244311
March 17, 2026

We hereby attest to the truth of the following facts:

We have not discussed the HTML language code in our program with anyone
other than our instructor or the teaching assistants assigned to this course.

We have not used HTML language code obtained from another student, or
any other unauthorized source, either modified or unmodified.

If any HTML language code or documentation used in our program was
obtained from another source, such as a textbook or course notes, that has been clearly noted with proper citation in the
comments of our program.
'''

from django.db import models

# Create your models here.

class Supplier(models.Model): 
    name = models.CharField(max_length=100) 
    city = models.CharField(max_length=100) 
    country = models.CharField(max_length=100) 
    created_at = models.DateTimeField() 
    
    def getName(self): 
        return self.name 
    
    def __str__(self): 
        return f"{self.name} - {self.city}, {self.country} created_at: {self.created_at}"

class WaterBottle(models.Model): 
    SKU = models.CharField(max_length=10, unique=True) 
    brand = models.CharField(max_length=100) 
    cost = models.DecimalField(max_digits=10, decimal_places=2) 
    size = models.CharField(max_length=50) 
    mouth_size = models.CharField(max_length=50) 
    color = models.CharField(max_length=50) 
    supplied_by = models.ForeignKey(Supplier, on_delete=models.CASCADE) 
    current_quantity = models.IntegerField() 
    
    def __str__(self): 
        return (f"{self.SKU}: {self.brand}, {self.mouth_size}, {self.size}, {self.color}, " f"supplied by {self.supplied_by.name}, Cost: {self.cost} : {self.current_quantity}")
    
class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def __str__(self):
        return self.username