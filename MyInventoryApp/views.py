from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Supplier, WaterBottle

# Global variable to track logged-in account
current_account = None

def login(request):
    global current_account
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            account = Account.objects.get(username=username, password=password)
            current_account = account
            return redirect('view_supplier')
        except Account.DoesNotExist:
            return render(request, 'MyInventoryApp/login.html', {'error': 'Invalid login'})
    success = request.GET.get('success')
    return render(request, 'MyInventoryApp/login.html', {'success': success})

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Account.objects.filter(username=username).exists():
            return render(request, 'MyInventoryApp/signup.html', {'error': 'Account already exists'})
        Account.objects.create(username=username, password=password)
        return redirect('/login/?success=Account created successfully')
    return render(request, 'MyInventoryApp/signup.html')

def view_supplier(request):
    suppliers = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {
        'suppliers': suppliers,
        'account': current_account
    })

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
        current_quantity = request.POST.get('current_quantity')
        supplied_by_pk = request.POST.get('supplied_by')
        supplier = get_object_or_404(Supplier, pk=supplied_by_pk)
        WaterBottle.objects.create(
            SKU=sku,
            brand=brand,
            price=price,
            size=size,
            mouth_size=mouth_size,
            color=color,
            current_quantity=current_quantity,
            supplied_by=supplier
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
    current_account = None
    return redirect('login')

def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if current_password != account.getPassword():
            return render(request, 'MyInventoryApp/change_password.html', {
                'account': account,
                'error': 'Current password is incorrect'
            })
        if new_password != confirm_password:
            return render(request, 'MyInventoryApp/change_password.html', {
                'account': account,
                'error': 'New passwords do not match'
            })
        Account.objects.filter(pk=pk).update(password=new_password)
        return redirect('manage_account', pk=pk)
    return render(request, 'MyInventoryApp/change_password.html', {'account': account})

def logout(request):
    global current_account
    current_account = None
    return redirect('login')