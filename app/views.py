from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.
def about(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'about.html',{'uid':uid})
    except:
        return render(request,'about.html')

def blog_details(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'blog-details.html',{'uid':uid})
    except:
        return render(request,'blog-details.html')

def blog(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'blog.html',{'uid':uid})
    except:
        return render(request,'blog.html')

def checkout(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'checkout.html',{'uid':uid})
    except:
        return render(request,'checkout.html')

def contact(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'contact.html',{'uid':uid})
    except:
        return render(request,'contact.html')

def elements(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'elements.html',{'uid':uid})
    except:
        return render(request,'elements.html')


def index(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        buy = Buy.objects.all()
        return render(request,'index.html',{'uid':uid,'buys':buy})
    except:
        return render(request,'index.html')
    # return render(request,'index.html')

def delivered(request,pk):
    buy = Buy.objects.get(id=pk)
    buy.status = True
    buy.save()
    return redirect('index')



def confirmation(request):
    uid = User.objects.get(email=request.session['email'])
    return render(request,'confirmation.html',{'uid':uid})

def login(request):
    if request.method == 'POST':
        try:
            uid = User.objects.get(email=request.POST['email'])
            if request.POST['password'] == uid.password:
                request.session['email'] = request.POST['email']
                uid = User.objects.get(email=request.POST['email'])
                return render(request,'index.html',{'uid':uid})
            else:
                msg = 'Password does not matched'
                return render(request,'login.html',{'msg':msg})
        except:
            msg = 'Email is not register'
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')

def register(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            User.objects.get(email = email)
            msg = 'Email aready exist'
            return render(request,'register.html',{'msg':msg})
        except:

            if request.POST['password'] == request.POST['cpassword']:
                global temp
                temp = {
                   'username' : request.POST['username'],
                    'email' : email,
                    'mobile' : request.POST['mobile'],
                    'password' : request.POST['password'],
                    'role' : request.POST['role']
                }
                otp = str(randrange(1000,9999))
                subject = 'Welcome to App '
                message = f'Hello {email}!! YOur OTP is {otp}.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'otp.html',{'otp':otp})

            else:
                msg = 'Password and Confirm Password does not matched'
                return render(request,'register.html',{'msg':msg})

    else:
        return render(request,'register.html')


def otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        uotp = request.POST['uotp']
        if otp == uotp:
            global temp
            User.objects.create(
                username = temp['username'],
                email = temp['email'],
                mobile = temp['mobile'],
                password = temp['password'],
                role = temp['role'],
                # pic = tem['pic']
            )
            del temp
            return render(request,'login.html',{'msg':"Account has been created"})
        else:
            msg = 'OTP does not matched'
            return render(request,'OTP.html',{'msg':msg,'otp':otp})
    else:   
        return render(request,'OTP.html')

def logout(request):
    del request.session['email']
    return redirect('index')

def profile(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        uid.username = request.POST['username']
        uid.mobile = request.POST['mobile']
        uid.password = request.POST['password']
        if 'pic' in request.FILES:
            uid.pic = request.FILES['pic']
        uid.save()
    return render(request,'profile.html',{'uid':uid})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            User.objects.get(email=email)
            otp = randrange(1000,9999)
            subject = 'OTP verify'
            message = f'hello your otp is {otp}. for forgot pasword'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'for-pass2.html',{'email':email,'otp':otp})
        except:
            msg = 'Email is not register'
            return render(request,'for-pass.html',{'msg':msg})

def forgot_password2(request):
    if request.method == "POST":
        email = request.POST['email']
        otp = request.POST['otp']
        uotp = request.POST['uotp']

        if otp == uotp:
            return render(request,'for-pass3.html',{'email':email})
        else:
            msg = 'OTP does not matched'
            return render(request,'for-pass2.html',{'msg':msg,'otp':otp,'email':email})

def forgot_password3(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        cpass = request.POST['cpassword']
        if password == cpass:
            uid = User.objects.get(email=email)
            uid.password = cpass
            uid.save()
            msg = 'Password updated successfully'
            return render(request,'login.html',{'msg':msg})
        else:
            msg = 'password are not getting matched'
            return render(request,'for-pass3.html',{'msg':msg,'email':email})

def add_product(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        Product.objects.create(
            uid = uid,
            title = request.POST['title'],
            cate = request.POST['category'],
            des = request.POST['des'],
            price = request.POST['price'],
            pic = request.FILES['pro_pic']
        )
        msg = 'Product added'
        return render(request,'add-product.html',{'msg':msg,'uid':uid})
    else:
        return render(request,'add-product.html',{'uid':uid})


def all_product(request):
    uid = User.objects.get(email=request.session['email'])
    products = Product.objects.all()
    return render(request,'all-product.html',{'uid':uid,'products':products})

def delete_product(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('all-product')

def edit_product(request,pk):
    uid = User.objects.get(email=request.session['email'])
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.title = request.POST['title']
        product.des = request.POST['des']
        product.price = request.POST['price']
        product.cate = request.POST['category']
        if 'pro_pic' in request.FILES:
            product.pic = request.FILES['pro_pic']
        product.save()
        return redirect('all-product')
    return render(request,'edit-product.html',{'product':product,'uid':uid})

def shop(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        cat = request.POST['category']
        if cat == 'all':
            products = Product.objects.all().order_by('id')
            return render(request,'shop.html',{'products':products,'uid':uid})
        products = Product.objects.filter(cate=cat)
        # print(products)
        return render(request,'shop.html',{'products':products,'uid':uid})

    else:
        products = Product.objects.all()
        return render(request,'shop.html',{'products':products,'uid':uid})
    
def product_details(request,pk):
    uid = User.objects.get(email=request.session['email'])
    product = Product.objects.get(id=pk)
    buy = Buy.objects.filter(product=product)
    return render(request,'product_details.html',{'product':product,'uid':uid,'buys':buy})

def add_to_cart(request,pk):
    uid = User.objects.get(email=request.session['email'])
    product = Product.objects.get(id=pk)
    Cart.objects.create(
        uid = uid,
        product = product,
        quantity = 1
    )
    msg = 'Added to cart'
    return render(request,'product_details.html',{'product':product,'uid':uid,'msg':msg})

def cart(request):
    uid = User.objects.get(email=request.session['email'])
    cart = Cart.objects.filter(uid=uid)
    return render(request,'cart.html',{'cart':cart,'uid':uid})

def delete_cart(request,pk):
    cart = Cart.objects.get(id=pk)
    cart.delete()
    return redirect('cart')


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def buy_product(request,pk):
    currency = 'INR'
    global product
    product = Product.objects.get(id=pk)
    uid = User.objects.get(email=request.session['email'])
    amount = int(product.price)*100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['uid'] = uid
    context['product'] = product
    return render(request, 'buy-product.html',context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                uid = User.objects.get(email=request.session['email'])

                global product
                amount =  int(product.price)*100 # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    date = datetime.now()
                    day = int(date.strftime("%d"))
                    month = int(date.strftime('%m'))
                    year = int(date.strftime('%Y'))
                    if day > 23:
                        day = randrange(1,6)
                        month = month + 1
                        date = datetime(year,month,day)
                        print(date.strftime('%x'))
                    # print(day,month,year)
                        Buy.objects.create(
                        uid = uid,
                        product = product,
                        amount = product.price,
                        pay_id = payment_id,
                        expected_date = f'{year}-{month}-0{day}'
                        )

                    try:
                        product = Product.objects.get(id=product.id)
                        cart = Cart.objects.get(product=product)
                        cart.delete()
                    except:
                        pass
                    del product
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html',{'uid':uid})
                except:
                    del product
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html',{'uid':uid})
            else:
                try:
                    del product
                except:
                    pass
                uid = User.objects.get(email=request.session['email'])
 
                # if signature verification fails.
                return render(request, 'paymentfail.html',{'uid':uid})
        except:
            try:
                del product
            except:
                pass
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        try:
            product
        except:
            pass
       # if other than POST request is made.
        return HttpResponseBadRequest()

def order(request):
    uid = User.objects.get(email=request.session['email'])
    buys = Buy.objects.filter(uid=uid)
    return render(request,'order.html',{'uid':uid,'buys':buys})

def delete_order(request,pk):
    buy = Buy.objects.get(id=pk)
    buy.delete()
    return redirect('order')
