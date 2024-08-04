from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponse
from .models import Item,Interest,Hod,BandF,product_types,Product
from .forms import Itemform, Interestedform
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import sys

def home(request):
    product_type_param = request.GET.get('type', 'all')
    
    if product_type_param == 'all':
        items = Item.objects.filter(Approved=True, ProductCount__gt=0)
    else:
        items = Item.objects.filter(Approved=True, ProductCount__gt=0, ProductType=product_type_param)
    
    pptitem = Item.objects.filter(Approved=True, ProductCount__gt=0)
    slides = list(pptitem)  # Convert queryset to list
    flagh = False
    flagb = False
    bandf = BandF.objects.filter(BF_id=request.user.username).first()
    hod = Hod.objects.filter(hod_id=request.user.username).first()

    if bandf and check_password(bandf.BF_password, request.user.password):
        flagb = True
    if hod and check_password(hod.hod_password, request.user.password):
        flagh = True

    for item in items:
        interest_count = Interest.objects.filter(Item_id=item, Given=False, Approved=True).count()
        setattr(item, 'interest_count', interest_count)
    
    # Retrieve all product types
    product_type = product_types.objects.all()

    # Create a dictionary to hold products grouped by type
    grouped_products = {}

    # Loop through each product type and retrieve associated products
    for type in product_type:
        products = Product.objects.filter(product_type=type)
        grouped_products[type] = products
    
    # Paginate the items
    paginator = Paginator(items, 10)  # Show 4 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'slides': slides,
        'flagh': flagh,
        'flagb': flagb,
        'product_type': product_type_param,
        'grouped_products': grouped_products
    }

    return render(request, "asset/home.html", context)


def search_products(request):
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    if search_query:
        items = Item.objects.filter(ProductName__icontains=search_query, Approved=True, ProductCount__gt=0)
    else:
        items = Item.objects.filter(Approved=True, ProductCount__gt=0)

    data = []
    for item in items:
        interest_count = Interest.objects.filter(Item_id=item, Given=False, Approved=True).count()
        data.append({
            'id': item.id,
            'ProductName': item.ProductName,
            'ProductDesc': item.ProductDesc,
            'ProductImage': item.ProductImage.url,  # Assuming ProductImage is a FileField
            'interest_count': interest_count
        })

    # Paginate the search results
    paginator = Paginator(data, 10) # Display 12 items per page
    page_data = paginator.get_page(page)

    # Convert the QuerySet to a list to serialize it as JSON
    data = list(page_data)

    return JsonResponse(data, safe=False)

#to request an item
def request_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    flagh = False
    flagb = False
    bandf = BandF.objects.filter(BF_id=request.user.username).first()
    hod = Hod.objects.filter(hod_id=request.user.username).first()
    if bandf and check_password(bandf.BF_password, request.user.password):
        flagb = True
    if hod and check_password(hod.hod_password, request.user.password):
        flagh = True

    departments = Hod.objects.values_list('Department', flat=True).distinct()

    if request.method == "POST":
        emp_id = request.POST.get('empid')
        department = request.POST.get('dept')
        mobile_no = request.POST.get('Mobile')
        product_count = int(request.POST.get('quan'))
        
        if product_count <= item.ProductCount:
            interest = Interest(
                EmpID=emp_id,
                Department=department,
                MobileNo=mobile_no,
                Product_count=product_count,
                Item_id=item 
            )
            
            if item.FinanceType == '2':
                interest.Finance = False
            
            interest.save()
            return redirect("home")
        else:
            error_message = 'Product count exceeds the available quantity.'
            form = Interestedform()
            return render(request, "asset/request_item.html", {'item': item, 'form': form, 'flagh': flagh, 'flagb': flagb, 'error_message': error_message, 'departments': departments})
    else:
        form = Interestedform() 

    return render(request, "asset/request_item.html", {'item': item, 'form': form,'flagh': flagh,'flagb': flagb, 'departments': departments})

@login_required
def view_request_item(request):
    flagh = False
    flagb = False
    bandf = BandF.objects.filter(BF_id=request.user.username).first()
    hod = Hod.objects.filter(hod_id=request.user.username).first()

    if bandf and check_password(bandf.BF_password, request.user.password):
        flagb = True
    if hod and check_password(hod.hod_password, request.user.password):
        flagh = True
    requests_to_approve = []
    if hod and check_password(hod.hod_password, request.user.password):
        hod_department = hod.Department
        interests = Interest.objects.filter(Department=hod_department, Approved=False)
    return render(request, "asset/viewrequestinterest.html", {'interests': interests,'flagh':flagh,'flagb':flagb})

@login_required
def approve_request(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)
    item = interest.Item_id
    if item.ProductCount >= interest.Product_count:
        interest.Approved = True
        interest.save()
    return redirect('view_request_item')

#to post an item
def requestpost(request):
    flagh = False
    flagb = False
    bandf = BandF.objects.filter(BF_id=request.user.username).first()
    hod = Hod.objects.filter(hod_id=request.user.username).first()
    if bandf and check_password(bandf.BF_password, request.user.password):
        flagb = True
    if hod and check_password(hod.hod_password, request.user.password):
        flagh = True
    
    departments = Hod.objects.values_list('Department', flat=True).distinct()

    product_type = product_types.objects.all()

    # Create a dictionary to hold products grouped by type
    grouped_products = {}

    # Loop through each product type and retrieve associated products
    for type in product_type:
        products = Product.objects.filter(product_type=type)
        grouped_products[type] = products

    

    if request.method == "POST":
        emp_id = request.POST.get('empid')
        emp_name = request.POST.get('name')
        department = request.POST.get('dept')
        mobile_no = request.POST.get('Mobile')
        product_name = request.POST.get('pname')
        product_type = request.POST.get('pt')
        custom_product_type = request.POST.get('customTypeContainer')
        finance_type = request.POST.get('ft')
        product_desc = request.POST.get('desc')
        product_count = int(request.POST.get('quan'))
        product_image = request.FILES.get('imge')
        img = Image.open(product_image)
        img = img.convert('RGB')
        img.thumbnail((1024, 1024))
        output = BytesIO()
        img.save(output, format='JPEG')
        output.seek(0)
        product_image = InMemoryUploadedFile(
            output, 'ImageField', f"{product_image.name.split('.')[0]}.jpg", 'image/jpeg', sys.getsizeof(output), None
        )
        if product_type == 'others':
            product_type = custom_product_type
        item = Item(
            EmpID=emp_id,
            EmpName=emp_name,
            Department=department,
            MobileNo=mobile_no,
            ProductName=product_name,
            ProductType=product_type,
            FinanceType=finance_type,
            ProductDesc=product_desc,
            ProductCount=product_count,
            ProductImage=product_image,
        )
        item.save()
        
        return redirect("home")
    else:
        form = Itemform()

    return render(request, "asset/additem.html", {'form': form, 'flagh': flagh, 'flagb': flagb, 'departments': departments,'product_types': product_types,'grouped_products': grouped_products,})

@login_required
def view_request_post(request):
    flagh = False
    flagb = False
    bandf = BandF.objects.filter(BF_id=request.user.username).first()
    hod = Hod.objects.filter(hod_id=request.user.username).first()
    if bandf and check_password(bandf.BF_password, request.user.password):
        flagb = True
    if hod and check_password(hod.hod_password, request.user.password):
        flagh = True
    hod = Hod.objects.filter(hod_id=request.user.username).first()
    if hod and check_password(hod.hod_password,request.user.password):
        hod_department = hod.Department
        requests = Item.objects.filter(Department=hod_department,Approved=False)
    return render(request, "asset/viewrequestpost.html", {'items_to_approve': requests,'flagh':flagh,'flagb':flagb})

@login_required
def approve_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.Approved = True
    item.save()
    return redirect('view_request_post')

#to view the people interested in the items of your dept
@login_required
def view_interests(request):
    flagh = False
    flagb = False
    bandf = BandF.objects.filter(BF_id=request.user.username).first()
    hod = Hod.objects.filter(hod_id=request.user.username).first()
    if bandf and check_password(bandf.BF_password, request.user.password):
        flagb = True
    if hod and check_password(hod.hod_password, request.user.password):
        flagh = True
    if not hod:
        return HttpResponse("You are not authorized to view this page.")
    items = Item.objects.filter(Department=hod.Department, ProductCount__gt=0)
    paginated_items = []
    for item in items:
        interests = Interest.objects.filter(Item_id=item, Given=False, Approved=True,valid=True)
        paginator = Paginator(interests, 4)  # Show 4 interests per page
        
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        paginated_items.append({
            'item': item,
            'page_obj': page_obj,
        })

    return render(request, "asset/view_interests.html", {'paginated_items': paginated_items,'flagh':flagh,'flagb':flagb})


@login_required
def approve_interest(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)
    item = interest.Item_id
    
    if item.ProductCount >= interest.Product_count:
        if item.FinanceType == "1":
            item.ProductCount -= interest.Product_count
        item.save()
        interest.Given = True
        interest.save()
        
        # Update other interests for the same item
        other_interests = Interest.objects.filter(Item_id=item, Product_count__gt=item.ProductCount, Given=False)
        for other_interest in other_interests:
            other_interest.valid = False
            other_interest.save()
    else:
        return JsonResponse({'message': 'Not enough items in stock to approve this request.'})
    
    return redirect('view_interests')


#finance approval
@login_required
def view_interests_finance(request):
    flagh = False
    flagb = False
    bandf = BandF.objects.filter(BF_id=request.user.username).first()
    hod = Hod.objects.filter(hod_id=request.user.username).first()
    if bandf and check_password(bandf.BF_password, request.user.password):
        flagb = True
    if hod and check_password(hod.hod_password, request.user.password):
        flagh = True
    items = Item.objects.filter(ProductCount__gt=0,FinanceType="2")
    paginated_items = []
    for item in items:
        interests = Interest.objects.filter(Item_id=item, Given=True,Approved=True,Finance = False)
        paginator = Paginator(interests, 4) 
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        paginated_items.append({
            'item': item,
            'page_obj': page_obj,
        })
    return render(request, "asset/finance.html", {'paginated_items': paginated_items,'flagh':flagh,'flagb':flagb})

@login_required
def approve_interest_finance(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)
    item = interest.Item_id
    if item.ProductCount >= interest.Product_count:
        item.ProductCount -= interest.Product_count
        item.save()
        interest.Finance = True
        interest.save()
        other_interests = Interest.objects.filter(Item_id=item, Product_count__gt=item.ProductCount, Given=False)
        for other_interest in other_interests:
            other_interest.valid = False
            other_interest.save()
    else:
        return JsonResponse({'message': 'Not enough items in stock to approve this request.'})
    return redirect('view_interests_finance')

def reject_interest_finance(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)
    item = interest.Item_id
    if item.ProductCount >= interest.Product_count:
        item.save()
        interest.Given = False
        interest.Finance = False
        interest.valid = False
        interest.save()
    else:
        return JsonResponse({'message': 'Not enough items in stock to approve this request.'})
    return redirect('view_interests_finance')

def displaysent(request):
    flagh = False
    flagb = False
    bandf = BandF.objects.filter(BF_id=request.user.username).first()
    hod = Hod.objects.filter(hod_id=request.user.username).first()
    if bandf and check_password(bandf.BF_password, request.user.password):
        flagb = True
    if hod and check_password(hod.hod_password, request.user.password):
        flagh = True
    hod_dept = hod.Department
    items = Item.objects.filter(Department=hod_dept)
    item_interests_dict = {}
    for item in items:
        interests = Interest.objects.filter(Item_id=item, Given=True, Finance=True)
        item_interests_dict[item] = interests

    items = Item.objects.filter(Department=hod.Department)
    paginated_items = []
    for item in items:
        interests = Interest.objects.filter(Item_id=item, Given=True, Finance=True)
        paginator = Paginator(interests, 4)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        paginated_items.append({
            'item': item,
            'page_obj': page_obj,
        })

    return render(request, "asset/display.html", {'paginated_items': paginated_items, 'default_view': 'sent','flagh':flagh,'flagb':flagb})

def displayreceived(request):
    flagh = False
    flagb = False
    bandf = BandF.objects.filter(BF_id=request.user.username).first()
    hod = Hod.objects.filter(hod_id=request.user.username).first()
    if bandf and check_password(bandf.BF_password, request.user.password):
        flagb = True
    if hod and check_password(hod.hod_password, request.user.password):
        flagh = True
    hod_dept  = hod.Department
    Interests = Interest.objects.filter(Department=hod_dept,Given=True,Finance=True)
    return render(request,"asset/display.html",{'interests':Interests, 'default_view': 'received','flagh':flagh,'flagb':flagb})

#Auth
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'asset/login.html')
    elif request.method == 'POST':
        username = request.POST.get('login-email')
        password = request.POST.get('login-pass')
        try:
            user = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            user = None
        
        if user is None or not user.check_password(password):
            return render(request, 'asset/login.html', {'error': "Username or password is incorrect"})
        else:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        logout(request)
        return redirect('home')