# , ; Zale Sebastian Latonio, 242494 ; Nathan Riley Sy, 244311
# March , 2026 

'''
We hereby attest to the truth of the following facts:

We have not discussed the Python language code in our program with anyone
other than my instructor or the teaching assistants assigned to this course.

We have not used Python language code obtained from another student, or
any other unauthorized source, either modified or unmodified.

If any Python language code or documentation used in our program was
obtained from another source, such as a textbook or course notes, that has been clearly noted with proper citation in the
comments of my program.
'''

"""
URL configuration for MyInventorySystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MyInventoryApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('view_supplier', views.view_supplier, name='view_supplier'),
    path('view_bottles', views.view_bottles, name='view_bottles'),
    path('add_bottle', views.add_bottle, name='add_bottle'),
    path('', views.view_supplier, name='view_supplier'),
]
