from django.shortcuts import render
from django.http import HttpResponse
from . models import Product
from . models import Contact
from . models import Order
from . models import OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    #products=Product.objects.all()
    #n=len(products)
    #nslides=n//4 + ceil((n/4)-(n//4))
    allprods=[] #empty list
    catprods = Product.objects.values('catogory','id') #it takes all catogories
    cats = {item["catogory"] for item in catprods} #set which stores unique catogories
    for cat in cats:
        prod = Product.objects.filter(catogory=cat) # it store all products belonging to that catogory
        n = len(prod)
        nslides=n//4 + ceil((n/4)-(n//4))  # it make number of slides required for that products
        
        allprods.append([prod,range(1,nslides),nslides])

    
    params={'allprods':allprods}
    

    return render(request,'shop/index.html',params)



def about(request):
    return render(request,'shop/about.html')

# to get anything from the html we are using request.method post
# but if we want to get it from admin we are using modelclassname.objects.filter
# and if u want to get backend funtionality like if u press button info about that stored in admin will be shown - for that pass it with id in url 
#    so that its id will be stored and we get that in views with id with that id you can show info related to that id

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noItem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')




def contact(request):
    thank=False
    if request.method=="POST":
        
        name =request.POST.get('name','') #name written in the get bracket is the name of the name button in html file 
        email=request.POST.get('email','')#email written in the get bracket is the name of the email button in html file 
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank=True

    return  render(request,'shop/contact.html',{'thank':thank})


def searchmatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.catogory.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprods=[] #empty list
    catprods = Product.objects.values('catogory','id') #it takes all catogories
    cats = {item["catogory"] for item in catprods} #set which stores unique catogories
    for cat in cats:
        prodtemp = Product.objects.filter(catogory=cat) # it store all products belonging to that catogory
        prod=[item for item in prodtemp if searchmatch(query,item)]
        n= len(prod)
        nslides=n//4 + ceil((n/4)-(n//4))  # it make number of slides required for that products
        if len(prod) !=0:
            allprods.append([prod,range(1,nslides),nslides])

    
    params={'allprods':allprods, "msg":""}
    if len(allprods) == 0 or len(query)<4:
        params = {'msg':"Please make sure to add relevant search query"}
    

    return render(request,'shop/search.html',params)




def prodview(request,myid):
    # fetch the product using the id
    product=Product.objects.filter(id=myid)

    return  render(request,"shop/prodview.html",{'product':product[0]})



def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update= OrderUpdate(order_id=order.order_id, update_desc="the order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')
    
