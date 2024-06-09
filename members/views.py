import math
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from . import views
from members.models import Produk, Vendor, Transaction
from members.forms import ProductForm
import pickle
import pandas as pd
import numpy as np

model = pickle.load(open('rf.pkl','rb'))

def welcome(request):
    
    products = Produk.objects.all() # it's select query,select all data store in products varible
    vendors = Vendor.objects.all()
    demand_prediction = None
    restock = None
    data = request.GET.get('predict')
    stock = request.GET.get('Stock')
    produk = None
    if data:
        # Extract input values from the GET request
        diskon = request.GET.get('Diskon (%)')
        shelf_life = request.GET.get('Shelf life (D)')
        hari = request.GET.get('Hari')
        harga = request.GET.get('Harga')
        kategori = request.GET.get('Kategori')
        vendor = request.GET.get('Vendor')
        cuaca = request.GET.get('Cuaca')
        holiday = request.GET.get('Holiday')
        produk = request.GET.get('Produk')

        # Ensure all required inputs are provided
        # if not all([diskon, shelf_life, hari, harga, kategori, vendor, cuaca, holiday]):
        #     return JsonResponse({'error': 'All fields are required.'})

        # Prepare the data in the format expected by the model
        data = {
            'Product ID': [1037],
            'Diskon (%)': [diskon],
            'Shelf life (D)': [shelf_life],
            'Weekend': [1 if hari in ['5','6'] else 0],
            'Weekday': [hari],
            'Harga': [harga],
            'Kategori': [kategori],
            'Vendor': [vendor],
            'Cuaca': [cuaca],
            'Holiday': [holiday],
            'Nama Produk': [produk]
        }
        print(data)

        # Convert to DataFrame
        input_df = pd.DataFrame(data)

        # Check the input DataFrame
        demand_prediction = int(model.predict(input_df)[0])
        # demand_prediction = 1
        restock = math.floor(int(stock) / int(demand_prediction))
    return render(request,"index.html",{'products': products, 'vendors': vendors, 'demand_prediction': demand_prediction, 'stock': stock, 'restock': restock, 'produk_name': produk})

def dashboard(request):
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render())

def logout(request):
    if(request.user.is_authenticated):
        auth_logout(request)
        return redirect('login')
    else :
        return redirect('login')
    
@csrf_exempt
def loginT(request):
    if(request.user.is_authenticated):
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            user = User.objects.get(email=request.POST['email'])
            authenticate(username=user.username, password=request.POST['password'])
            if(user is not None):            
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('login')
        else:
            template = loader.get_template('login.html')
            return HttpResponse(template.render())
        
# def logout(request):

    
def product(request):
    if(request.user.is_authenticated):
        products = Produk.objects.all() # it's select query,select all data store in products varible
        return render(request,"product/product.html",{'products': products})
    else:
        return redirect('login')
    
def productAdd(request):
    if(request.user.is_authenticated):
        if request.method == "POST":
            form = ProductForm(request.POST) # here "form" is one varible
            if form.is_valid():
                form.save()
                return redirect("product")
        else:
            form = ProductForm()

        return render(request,"product/create.html",{'form':form})
    else:
        return redirect('login')
      

def productEdit(request,id):     
    if(request.user.is_authenticated):
        if request.method == "POST":
            produk = Produk.objects.get(id=id)
            form = ProductForm(request.POST, instance=produk)
            print(form.errors)
            if form.is_valid():
                form.save()
                return redirect('product')
        else:
            product = Produk.objects.get(id=id)
            return render(request,"product/edit.html",{'product':product})
    else:
        return redirect('login')

def productUpdate(request,id):
	employee = Employee.objects.get(id=id)
	form = EmployeeForm(request.POST, instance=employee)
	if form.is_valid():
		form.save()
		return redirect('/show')
	return render(request,"product/edit.html",{'employee':employee})

def productDelete(request,id):
	employee = Produk.objects.get(id=id)
	employee.delete()
	return redirect("/product")

def vendor(request):
    if(request.user.is_authenticated):
        # it's select query,select all data store in employees varible
        vendors = Vendor.objects.all()
        return render(request, "vendor/index.html", {'vendors': vendors})
    else:
        return redirect('login')


def vendorAdd(request):
    if(request.user.is_authenticated):
        if request.method == "POST":
            try:
                vendor = Vendor.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    mobile_no=request.POST['mobile_no'],
                    location=request.POST['location'],
                )
                return redirect("/vendor")
            except:
                pass

        return render(request, "vendor/create.html")
    else:
        return redirect('login')


def vendorEdit(request, id):
    if(request.user.is_authenticated):
        if request.method == "POST":
            vendor = Vendor.objects.get(id=id)

            vendor.name=request.POST['name']
            vendor.email=request.POST['email']
            vendor.mobile_no=request.POST['mobile_no']
            vendor.location=request.POST['location']
            vendor.save()
            return redirect('/vendor')
        else:
            vendor = Vendor.objects.get(id=id)
            return render(request, "vendor/edit.html", {'vendor': vendor})
    else:
        return redirect('login')

def vendorDelete(request, id):
    if(request.user.is_authenticated):
        vendor = Vendor.objects.get(id=id)
        vendor.delete()
        return redirect("/vendor")
    else:
        return redirect('login')

def transaction(request):
    if(request.user.is_authenticated):
        # it's select query,select all data store in employees varible
        transactions = Transaction.objects.all()
        produks = Produk.objects.all()
        vendors = Vendor.objects.all()
        return render(request, "transaction/index.html", {'transactions': transactions, 'produks': produks, 'vendors': vendors})
    else:
        return redirect('login')


def transactionAdd(request):
    if(request.user.is_authenticated):
        if request.method == "POST":
            # try:
                transaction = Transaction.objects.create(
                    date=request.POST['tanggal'],
                    demand=request.POST['demand'],
                    stock=request.POST['stock'],
                    rusak=request.POST['rusak'],
                    holiday=request.POST['holiday'],
                    diskon=request.POST['diskon'],
                    men=request.POST['men'],
                    women=request.POST['women'],
                    restok=request.POST['restok'],
                    vendor_id=request.POST['vendor_id'],
                    product_id=request.POST['product_id'],
                    jumlah_restok=request.POST['jumlah_restok'] if request.POST['jumlah_restok'] else 0,
                )
                return redirect("/transaction")
            # except:
            #     pass

        produks = Produk.objects.all()
        vendors = Vendor.objects.all()
        return render(request, "transaction/create.html", {'produks': produks, 'vendors': vendors})
    else:
        return redirect('login')


def transactionEdit(request, id):
    if(request.user.is_authenticated):
        if request.method == "POST":
            transaction = Transaction.objects.get(id=id)

            transaction.date=request.POST['tanggal']
            transaction.demand=request.POST['demand']
            transaction.stock=request.POST['stock']
            transaction.rusak=request.POST['rusak']
            transaction.holiday=request.POST['holiday']
            transaction.diskon=request.POST['diskon']
            transaction.men=request.POST['men']
            transaction.women=request.POST['women']
            transaction.restok=request.POST['restok']
            transaction.vendor_id=request.POST['vendor_id']
            transaction.product_id=request.POST['product_id']
            transaction.jumlah_restok=request.POST['jumlah_restok'] if request.POST['jumlah_restok'] else 0
            transaction.save()
            return redirect('/transaction')
        else:
            
            produks = Produk.objects.all()
            vendors = Vendor.objects.all()
            transaction = Transaction.objects.get(id=id)
            return render(request, "transaction/edit.html", {'transaction': transaction, 'produks': produks, 'vendors': vendors})
    else:
        return redirect('login')

def transactionDelete(request, id):
    if(request.user.is_authenticated):
        transaction = Transaction.objects.get(id=id)
        transaction.delete()
        return redirect("/transaction")
    else:
        return redirect('login')
# Create your views here.
