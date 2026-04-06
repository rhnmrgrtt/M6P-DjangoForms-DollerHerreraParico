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

from django.contrib import admin

# Register your models here.
from .models import Supplier, WaterBottle

admin.site.register(Supplier)
admin.site.register(WaterBottle)