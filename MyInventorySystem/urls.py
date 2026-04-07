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
from django.contrib import admin
from django.urls import path
from MyInventoryApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('view_supplier/', views.view_supplier, name='view_supplier'),
    path('view_bottles/', views.view_bottles, name='view_bottles'),
    path('view_bottle_details/<int:pk>/', views.view_bottle_details, name='view_bottle_details'),
    path('add_bottle/', views.add_bottle, name='add_bottle'),
    path('manage_account/<int:pk>/', views.manage_account, name='manage_account'),
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
]
