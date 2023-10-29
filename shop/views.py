from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from django.http import JsonResponse
from .forms import *
import json
from myshop.settings import MEDIA_ROOT, MEDIA_URL,STATIC_URL
from django.core.paginator import Paginator
# Create your views here.

def store_view(request):
    pageno=1
    try:
        pageno=request.GET.get['n']
    except:
        pass
    
    prods=Product.objects.all()
    p=Paginator(prods,9)
    page = p.get_page(pageno)
    context={'MEDIA_URL':MEDIA_URL,'page':page}#'context':prods, 
    return render(request, 'store.html',context)


def cart_view(request):
    mediaurl=MEDIA_URL

    ########### if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()

        x=0
        q=0
        for item in items:
            x+=item.get_total
            q+=item.quantity
            
        context= {'items':items, 'MEDIA_URL':mediaurl,'x':x,'q':q}
        print(items)
        return render(request, 'cart.html',context)
 

    ##############3 if user is not authenticated
    else:
        #using try because cart cookie might not be present
        try:
            cart = json.loads(request.COOKIES['cart']) # it will be turned to a python dictionary, get cart
        except:
            cart={}

        items=[] #list of cart items
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartitems= order['get_cart_items'] 
        colors=[]

        for i in cart: #for item in cart, get the color  of that item
            color=cart[i] #get item color
            if 'None' in color:
                colors.append('None')
            elif 'color1' in color:
                colors.append('color1')
            elif 'color2' in color:
                colors.append('color2')
            elif 'color3' in color:
                colors.append('color3')
            else:
                colors.append('color4')

        x=0 #absolute total price
        q=0 #absolute total number of items in cart
        c=-1
        for i in cart:     #for item in cart
            c+=1
            try:
                cartitems += cart[i][colors[c]]['quantity'] #get quantity of item
            except KeyError:
                pass
            
            keys_array = []
            colors_array = []
            quantities_array = []
            
            for key, value in cart.items(): 
                
                keys_array.append(key)
                #key=product id, value= rest of dictionry of productid{} 

                for color,quantity in value.items():
                    #quantities_array.append(quantity['quantity'])

                    product=Product.objects.get(id=i)
                    #print('xx',i,cart[i],color)
                    try:
                        total=(product.price * cart[i][color]['quantity'])
                        order['get_cart_total']+=total
                        order['get_cart_items']+=cart[i][color]['quantity']
                        #print(cart[i][color]['quantity'])
                        item = {
                        'product':{
                            'id': product.id,
                            'name':product.name,
                            'price':product.price,
                            'image':product.image,
                            'image2':product.image2,
                            'image3':product.image3,
                            'image4':product.image4,
                            'color1':product.color1,
                            'color2':product.color2,
                            'color3':product.color3,
                            'color4':product.color4,
                            },
                        'color':color,
                        'quantity':cart[i][color]['quantity'],
                        'get_total':total,
                        }
                        if items==[]:
                            items.append(item)
                            x+=total
                            q+=cart[i][color]['quantity']
                        elif item!=items[len(items)-1]:
                            items.append(item)
                            x+=total
                            q+=cart[i][color]['quantity']
                    except:
                        pass

 
    context={'items':items, 'order':order, 'cartitems':cartitems,'MEDIA_URL':mediaurl,'x':x,'q':q}
    return render(request, 'cart.html',context)


def product_view(request):
    x=request.GET.get('id', 1)
    product=Product.objects.get(id=x)
    mediaurl=MEDIA_URL
    return render(request, 'product.html',{'product':product,'MEDIA_URL':mediaurl,})
    

def checkout_view(request):
    mediaurl=MEDIA_URL
    if request.user.is_authenticated:
        if request.method == "POST":
            form=ShippingForm(request.POST)
            if form.is_valid():
                #fill in the shipping model
                customer = request.user.customer
                order=Order.objects.get(customer=customer)
                ship=ShippingAddress(customer=customer,order=order,
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    zipcode=form.cleaned_data['zipcode'],
                    date_added='now')
                ship.save()
                
                return HttpResponseRedirect("/thanks/")

        else:
            customer = request.user.customer
            order,created=Order.objects.get_or_create(customer=customer, complete=False)
            items= order.orderitem_set.all()
            print(items)
            context={'order':order,'items':items, 'form':ShippingForm(),'MEDIA_URL':mediaurl}
            return render(request, 'checkout.html',context)    
            
    else:
        #using try because cart cookie might not be present
        try:
            cart = json.loads(request.COOKIES['cart']) # it will be turned to a python dictionary
        except:
            cart={}
            return render(request, 'checkout.html',{'form':ShippingForm()})

        if request.method == "POST":
            form=ShippingForm(request.POST)
            if form.is_valid():
                #fill in the shipping model
                customer = Customer(name=form.cleaned_data['fullname'],email='addlate@rsdkj.s')
                customer.save() 
                order=Order(customer=customer)
                order.save()
                ship=ShippingAddress(customer=customer,order=order,
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    zipcode=form.cleaned_data['zipcode'],
                    date_added='now')
                ship.save()

                #get items from cart
                products=[]
                colors=[]
                quantities=[]
                c=0
                for i in cart:
                    products.append(i)
                    color=cart[i] #get item color
                    if 'None' in color:
                        colors.append('None')
                    elif 'color1' in color:
                        colors.append('color1')
                    elif 'color2' in color:
                        colors.append('color2')
                    elif 'color3' in color:
                        colors.append('color3')
                    else:
                        colors.append('color4')
                    quantities.append(cart[i][colors[c]]['quantity'])

                #print(products)

                c=0
                for item in products:
                    product=products[c]
                    color=colors[c]
                    quantity=quantities[c]
                    #print(color,product,quantity)
                    product=Product.objects.filter(id=products[c]).first()
                    orderitem,created=OrderItem.objects.get_or_create(order=order,color=color,
                                                                      product=product,quantity=quantity)
                    orderitem.save()
                    c+=1
                    
                
                return HttpResponseRedirect("/thanks/")

    order=''
    if True: 
        #using try because cart cookie might not be present
        try:
            cart = json.loads(request.COOKIES['cart']) # it will be turned to a python dictionary, get cart
        except:
            cart={}

        items=[] #list of cart items
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartitems= order['get_cart_items'] 
        colors=[]

        for i in cart: #for item in cart, get the color  of that item
            color=cart[i] #get item color
            if 'None' in color:
                colors.append('None')
            elif 'color1' in color:
                colors.append('color1')
            elif 'color2' in color:
                colors.append('color2')
            elif 'color3' in color:
                colors.append('color3')
            else:
                colors.append('color4')

        c=0 #counter
        for i in cart:     #for item in cart               
            try:
                cartitems += cart[i][colors[c]]['quantity'] #get quantity of item
            except KeyError:
                items=[]
                order=[]
                cartitems=[]
                break

            keys_array = []
            colors_array = []
            quantities_array = []
            x=0
            q=0
            for key, value in cart.items(): 
                
                keys_array.append(key)

                for color, quantity in value.items():

                    colors_array.append(color)
                    quantities_array.append(quantity['quantity'])

                    product=Product.objects.get(id=i)
                    try:
                        total=(product.price * cart[i][colors[c]]['quantity'])
                        order['get_cart_total']+=total
                        order['get_cart_items']+=cart[i][colors[c]]['quantity']
                        item = {
                        'product':{
                            'id': product.id,
                            'name':product.name,
                            'price':product.price,
                            'image':product.image,
                            'image2':product.image2,
                            'image3':product.image3,
                            'image4':product.image4,
                            'color1':product.color1,
                            'color2':product.color2,
                            'color3':product.color3,
                            'color4':product.color4,
                            },
                        'color':color,
                        'quantity':cart[i][color]['quantity'],
                        'get_total':total,
                        }

                        if items==[]:
                            items.append(item)
                            x+=total
                            q+=cart[i][color]['quantity']
                        elif item!=items[len(items)-1]:
                            items.append(item)
                            x+=total
                            q+=cart[i][color]['quantity']
                    except:
                        pass

                    
            c+=1
    context={'order':order,'items':items, 'form':ShippingForm(),'MEDIA_URL':mediaurl}
    return render(request, 'checkout.html',context)    
        

    
def update_cart(request):
    data=json.loads(request.body)
    productId= data['productid']
    action=data['action']
    try:
        color=data['color']
    except:
        color='color1'
        
    #create order
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created=OrderItem.objects.get_or_create(order=order,color=color,product=product)

    if action=='add':
        orderitem.quantity=(orderitem.quantity+1)
    elif action=='remove':
        orderitem.quantity=(orderitem.quantity-1)

    if orderitem.quantity <=0:
        orderitem.delete()
    else:
        orderitem.save()

    return JsonResponse('Item was added',safe=False)

'''
cart={"1":{"None":{"quantity":8},"color1":{"quantity":2},"color2":{"quantity":1}}}'''
