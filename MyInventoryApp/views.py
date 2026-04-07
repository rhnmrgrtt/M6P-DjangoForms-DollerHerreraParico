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

from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, WaterBottle, Account

# Global variable to track logged-in account (as taught in class)
current_account = None

def login_view(request):
    global current_account
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            account = Account.objects.get(username=username, password=password)
            current_account = account  # store in global variable
            return redirect('view_supplier')
        except Account.DoesNotExist:
            return render(request, 'MyInventoryApp/login.html', {'error': 'Invalid login'})
    return render(request, 'MyInventoryApp/login.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Account.objects.filter(username=username).exists():
            return render(request, 'MyInventoryApp/signup.html', {'error': 'Account already exists'})
        Account.objects.create(username=username, password=password)
        return render(request, 'MyInventoryApp/login.html', {'success': 'Account created successfully'})
    return render(request, 'MyInventoryApp/signup.html')

def view_supplier(request):
    suppliers = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {'suppliers': suppliers, 'account': current_account})

def view_bottles(request):
    bottles = WaterBottle.objects.all()
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles': bottles})

def view_bottle_details(request, pk):
    bottle = get_object_or_404(WaterBottle, pk=pk)
    return render(request, 'MyInventoryApp/view_bottle_details.html', {'bottle': bottle})

def delete_bottle(request, pk):
    WaterBottle.objects.filter(pk=pk).delete()
    return redirect('view_bottles')

def add_bottle(request):
    if request.method == "POST":
        sku = request.POST.get('sku')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        size = request.POST.get('size')
        mouth_size = request.POST.get('mouth_size')
        color = request.POST.get('color')
        supplier_id = request.POST.get('supplied_by')
        quantity = request.POST.get('current_quantity')
        supplier = get_object_or_404(Supplier, pk=supplier_id)
        WaterBottle.objects.create(
            SKU=sku, brand=brand, price=price, size=size,
            mouth_size=mouth_size, color=color,
            supplied_by=supplier, current_quantity=quantity
        )
        return redirect('view_supplier')
    suppliers = Supplier.objects.all()
    return render(request, 'MyInventoryApp/add_bottle.html', {'suppliers': suppliers})

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'MyInventoryApp/manage_account.html', {'account': account})

def delete_account(request, pk):
    global current_account
    Account.objects.filter(pk=pk).delete()
    current_account = None  # clear global variable
    return redirect('login')

def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        current = request.POST.get('current_password')
        new_pass = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')
        if current != account.password:
            return render(request, 'MyInventoryApp/change_password.html', {'account': account, 'error': 'Current password is incorrect'})
        if new_pass != confirm:
            return render(request, 'MyInventoryApp/change_password.html', {'account': account, 'error': 'New passwords do not match'})
        Account.objects.filter(pk=pk).update(password=new_pass)
        return redirect('manage_account', pk=pk)
    return render(request, 'MyInventoryApp/change_password.html', {'account': account})

def logout_view(request):
    global current_account
    current_account = None  # clear global variable on logout
    return redirect('login')