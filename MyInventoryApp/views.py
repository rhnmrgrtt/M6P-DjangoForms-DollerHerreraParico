from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Supplier, WaterBottle

current_account = None

def login(request):
    global current_account
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            return render(request, 'MyInventoryApp/login.html', {'error': 'Please fill in all fields'})
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
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            return render(request, 'MyInventoryApp/signup.html', {'error': 'Please fill in all fields'})
        if Account.objects.filter(username=username).exists():
            return render(request, 'MyInventoryApp/signup.html', {'error': 'Account already exists'})
        Account.objects.create(username=username, password=password)
        return redirect('/login/?success=Account created successfully')
    return render(request, 'MyInventoryApp/signup.html')

def view_supplier(request):
    if current_account is None:
        return redirect('login')
    suppliers = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {
        'suppliers': suppliers,
        'account': current_account
    })

def view_bottles(request, pk):
    if current_account is None:
        return redirect('login')
    supplier = get_object_or_404(Supplier, pk=pk)
    bottles = WaterBottle.objects.filter(supplied_by=supplier)
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles': bottles,'supplier': supplier,})

def view_bottle_details(request, pk):
    if current_account is None:
        return redirect('login')
    bottle = get_object_or_404(WaterBottle, pk=pk)
    return render(request, 'MyInventoryApp/view_bottle_details.html', {'bottle': bottle,})

def delete_bottle(request, pk):
    if current_account is None:
        return redirect('login')
    bottle = get_object_or_404(WaterBottle, pk=pk)
    supplier_pk = bottle.supplied_by.pk
    bottle.delete()
    return redirect('view_bottles', pk=supplier_pk)

def add_bottle(request):
    if current_account is None:
        return redirect('login')
    suppliers = Supplier.objects.all()
    if request.method == "POST":
        sku = request.POST.get('sku', '').strip()
        brand = request.POST.get('brand', '').strip()
        price = request.POST.get('price', '').strip()
        size = request.POST.get('size', '').strip()
        mouth_size = request.POST.get('mouth_size', '').strip()
        color = request.POST.get('color', '').strip()
        current_quantity = request.POST.get('current_quantity', '').strip()
        supplied_by_pk = request.POST.get('supplied_by')

        # Check empty fields
        if not all([sku, brand, price, size, mouth_size, color, current_quantity]):
            return render(request, 'MyInventoryApp/add_bottle.html', {
                'suppliers': suppliers,
                'error': 'Please fill in all fields'
            })

        # Check duplicate SKU
        if WaterBottle.objects.filter(SKU=sku).exists():
            return render(request, 'MyInventoryApp/add_bottle.html', {
                'suppliers': suppliers,
                'error': 'A water bottle with that SKU already exists'
            })

        # Check quantity not below 0
        try:
            quantity_int = int(current_quantity)
            if quantity_int < 0:
                return render(request, 'MyInventoryApp/add_bottle.html', {
                    'suppliers': suppliers,
                    'error': 'Quantity cannot be negative'
                })
        except ValueError:
            return render(request, 'MyInventoryApp/add_bottle.html', {
                'suppliers': suppliers,
                'error': 'Quantity must be a valid number'
            })

        # Check price is valid
        try:
            price_float = float(price)
            if price_float < 0:
                return render(request, 'MyInventoryApp/add_bottle.html', {
                    'suppliers': suppliers,
                    'error': 'Price cannot be negative'
                })
        except ValueError:
            return render(request, 'MyInventoryApp/add_bottle.html', {
                'suppliers': suppliers,
                'error': 'Price must be a valid number'
            })

        supplier = get_object_or_404(Supplier, pk=supplied_by_pk)
        WaterBottle.objects.create(
            SKU=sku,
            brand=brand,
            cost=price_float,
            size=size,
            mouth_size=mouth_size,
            color=color,
            current_quantity=quantity_int,
            supplied_by=supplier
        )
        return redirect('view_supplier')
    return render(request, 'MyInventoryApp/add_bottle.html', {
        'suppliers': suppliers,
        'account': current_account
    })

def manage_account(request, pk):
    if current_account is None:
        return redirect('login')
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'MyInventoryApp/manage_account.html', {'account': account})

def delete_account(request, pk):
    global current_account
    Account.objects.filter(pk=pk).delete()
    current_account = None
    return redirect('login')

def change_password(request, pk):
    if current_account is None:
        return redirect('login')
    account = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        current_password = request.POST.get('current_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not current_password or not new_password or not confirm_password:
            return render(request, 'MyInventoryApp/change_password.html', {
                'account': account,
                'error': 'Please fill in all fields'
            })
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
        if new_password == current_password:
            return render(request, 'MyInventoryApp/change_password.html', {
                'account': account,
                'error': 'New password cannot be the same as current password'
            })
        Account.objects.filter(pk=account.pk).update(password=new_password)
        return redirect('manage_account', pk=account.pk)
    return render(request, 'MyInventoryApp/change_password.html', {'account': account})

def logout(request):
    global current_account
    current_account = None
    return redirect('login')