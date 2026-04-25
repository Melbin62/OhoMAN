from django.contrib.admin import action
from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib import messages
import razorpay
from django.conf import settings
from django.db.models import Avg, Q
from  django.core.mail import send_mail


# Create your views here.

def customer_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phno = request.POST['phno']
        address = request.POST['address']
        password = request.POST['password']
        x = customer_reg.objects.filter(email=email)
        if list(x) == []:
            data = customer_reg.objects.create(name=name, email=email, phno=phno,  address=address)
            data.save()
            data1 = Login.objects.create(email=email, password=password, status=1)
            data1.save()
            return render(request, 'login.html')
        else:
            url = '/customer_registration/'
            msg = '''<script>alert('Email already exist')
                                window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
    else:
        return render(request, 'customer_registration.html')

def serviceprov_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phno = request.POST['phno']
        service = request.POST['service']
        baseprice = request.POST['baseprice']
        servicedetails = request.POST['servicedetails']
        location = request.POST['location']
        license = request.FILES['license']
        password = request.POST['password']
        x = serviceprov_reg.objects.filter(email=email)
        if list(x) == []:
            data = serviceprov_reg.objects.create(name=name, email=email, phno=phno,  location=location, service=service, baseprice=baseprice, servicedetails=servicedetails, license=license, status="pending")
            data.save()
            data1 = Login.objects.create(email=email, password=password, status=2)
            data1.save()
            return render(request, 'login.html')
        else:
            url = '/serviceprov_registration/'
            msg = '''<script>alert('Email already exist')
                                window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
    else:
        data = services.objects.all()
        return render(request, 'serviceprov_registration.html', {'data': data})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        try:
            x = Login.objects.get(email=email)
            print(x)
            if x.password == password:
                if x.status==1 :
                    request.session['uid'] = email
                    print(x.status)
                    return redirect(profile)
                elif x.status==2:
                    y = serviceprov_reg.objects.get(email=email)
                    if y.status == 'confirm':
                        request.session['sid']= email
                        return redirect(profile)
                    else:
                        messages.info(request, 'login failed,request is processing...')
                        return render(request,'login.html')
                else:
                    request.session['aid'] = email
                    return redirect(profile)
            else:
                messages.info(request, 'login failed,password incorrect...')
                return render(request, 'login.html')
        except Exception:
            messages.info(request, 'login failed,incorrect email...')
            return render(request, 'login.html')
    else:
        return render(request,'login.html')


def profile(request):
    if 'uid' in request.session:
        data = services.objects.all()
        customer_email = request.session['uid']
        customer_obj = customer_reg.objects.get(email=customer_email)

        return render(request, 'service_homepage.html',{'data': data,'customer': customer_obj})

    elif 'sid' in request.session:
        serviceprov_email = request.session['sid']
        serviceprov_obj = serviceprov_reg.objects.get(email=serviceprov_email)
        data1 = booking.objects.filter(serviceprov=serviceprov_obj, status='Confirm').count()
        data2 = booking.objects.filter(serviceprov=serviceprov_obj, status='pending').count()

        return render(request, 'servicepov_dashboard.html', {'data1': data1, 'data2': data2})

    elif 'aid' in request.session:
        data1 = serviceprov_reg.objects.filter(status='confirm').count()
        data2 = serviceprov_reg.objects.filter(status='pending').count()  # Added () here

        return render(request, 'admin_dashboard.html', {'data1': data1,'data2': data2})
    else:
        data = services.objects.all()
        return render(request, 'home.html',{'data': data})

def logout(request):
    if 'uid' in request.session or 'sid' in request.session  or 'aid' in request.session:
        request.session.flush()
        return redirect(login)
    else:
        return redirect(login)

def servicepov_req(request):
    if request.method=='GET':
        data = serviceprov_reg.objects.filter(status='pending')
        return render(request, 'servicepov_req.html', {'data': data})
    else:
        return render(request, 'admin_dashboard.html')


def approved_providers(request):
    if request.method == 'POST':
        id = request.POST['id']
        d = serviceprov_reg.objects.get(id=id)
        d.status = 'confirm'
        d.save()
        b = d.email
        send_mail('Account Created', 'Your request has been approved',
                  'settings.EMAIL_HOST_USER', [b], fail_silently=False)
        return redirect(servicepov_req)
    else:
        return render(request, '.html')


def reject_providers(request):
    if request.method=='POST':
        id = request.POST['id']
        d = serviceprov_reg.objects.get(id=id)
        b=d.email
        d.delete()
        send_mail('Account Not Created', 'Your request has not been approved',
                  'settings.EMAIL_HOST_USER', [b], fail_silently=False)
        return redirect(servicepov_req)
    else:
        return render(request,'admin_dashboard.html')


def view_approvedpov(request):
    if request.method=='GET':
        data = serviceprov_reg.objects.filter(status='confirm')
        return render(request, 'approved_providers.html', {'data': data})
    else:
        return render(request, 'admin_dashboard.html')


def remove_approvepov(request):
    if request.method=='POST':
        id = request.POST['id']
        d = serviceprov_reg.objects.get(id=id)
        b=d.email
        d.delete()
        send_mail('Removed', 'you removed from  Website',
                  'settings.EMAIL_HOST_USER', [b], fail_silently=False)
        return redirect(view_approvedpov)
    else:
        return render(request,'admin_dashboard.html')


def add_service(request):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES['image']
        data =services.objects.create(name=name, image=image)
        data.save()
        data = services.objects.all()
        return render(request, 'add_service.html', {'data': data})
    else:
        data = services.objects.all()
        return render(request,'add_service.html',{'data':data})

def remove_service(request):
    if request.method=='POST':
        id = request.POST['id']
        d = services.objects.get(id=id)
        d.delete()
        return redirect(add_service)
    else:
        return render(request,'admin_dashboard.html')


def servicebooking_req(request):
    serviceprov_email = request.session['sid']
    bookings = booking.objects.select_related(
        'customer', 'serviceprov'
    ).filter(
        serviceprov__email=serviceprov_email,
        status='pending'
    )
    return render(request, 'servicebooking_req.html', {'bookings': bookings})


def approve_booking(request):
    if request.method=='POST':
        serviceprov_email=request.session['sid']
        serviceprov_id = serviceprov_reg.objects.get(email=serviceprov_email)
        customer_id=request.POST['customer_id']
        booking_id = request.POST['booking_id']
        booking.objects.filter(
            id=booking_id,
            serviceprov_id=serviceprov_id.id,
            customer_id=customer_id
        ).update(status='Confirm')
        c=customer_reg.objects.get(id= customer_id)
        d=c.email

        send_mail(' Booking Confirmed', 'your Booking is confirmed',
                  'settings.EMAIL_HOST_USER', [d], fail_silently=False)
        return redirect(servicebooking_req)
    else:
        return render(request, 'servicebooking_req.html')


def reject_booking(request):
    if request.method=='POST':
        serviceprov_email=request.session['sid']
        serviceprov_id = serviceprov_reg.objects.get(email=serviceprov_email)
        customer_id=request.POST['customer_id']
        booking_id = request.POST['booking_id']
        booking.objects.filter(
            id=booking_id,
            serviceprov_id=serviceprov_id.id,
            customer_id=customer_id
        ).update(status='Reject')
        c = customer_reg.objects.get(id= customer_id)
        d=c.email
        send_mail('Booking Rejected', 'Your Booking is rejected',
                  'settings.EMAIL_HOST_USER', [d], fail_silently=False)
        return redirect(servicebooking_req)
    else:
        return render(request, 'servicebooking_req.html')



def confirmed_booking(request):
    serviceprov_id = request.session['sid']  # doctor email
    bookings = booking.objects.select_related(
        'customer', 'serviceprov'
    ).filter(
        serviceprov__email=serviceprov_id,
        status='Confirm'
    )
    return render(request, 'confirmed_booking.html', {'bookings': bookings})


def service_booking(request):
    locations = serviceprov_reg.objects.filter(status='confirm').values('location').distinct()
    all_categories = services.objects.all()

    if request.method == 'POST':
        loc_query = request.POST.get('location')
        service_name_query = request.POST.get('servicename')
        query = Q(status='confirm')

        if loc_query:
            query &= Q(location=loc_query)

        if service_name_query:
            try:
                service_obj = services.objects.get(name=service_name_query)
                query &= Q(service=str(service_obj.id))
            except services.DoesNotExist:
                pass

        results = serviceprov_reg.objects.filter(query).annotate(
            avg_rating=Avg('booking__rating')
        )

        return render(request, 'service_booking.html', {
            'data1': locations, 'data2': all_categories, 'results': results
        })

    else:
        results = serviceprov_reg.objects.filter(status='confirm').annotate(
            avg_rating=Avg('booking__rating')
        )

        return render(request, 'service_booking.html', {
            'data1': locations, 'data2': all_categories, 'results': results
        })

def booking_form(request):
    if request.method=='POST':
        serviceprov_id = request.POST.get('id')
        request.session['serviceprov_id'] = serviceprov_id
        a = request.session['uid']
        data = serviceprov_reg.objects.filter(id=serviceprov_id)
        return render(request,'booking_form.html',{'data':data})
    else:
        return render(request, 'booking_form.html')

def booking_req(request):
    if request.method == 'POST':
        cust_email = request.session['uid']
        customer_id = customer_reg.objects.get(email=cust_email)
        serviceprov = request.session['serviceprov_id']
        serviceprov_id = serviceprov_reg.objects.get(id=serviceprov)
        print(serviceprov_id)
        date = request.POST['date']
        time=request.POST['time']
        msg = request.POST['msg']

        booking.objects.create(
            customer=customer_id,
            serviceprov=serviceprov_id,
            date=date,
            time=time,
            msg=msg
        )

        return redirect(service_booking)
    else:
        return render(request, 'service_homepage.html')

def booking_status(request):
    if request.method=='POST':
        booking_id=request.POST['booking_id']
        data = booking.objects.get(id=booking_id)
        return render(request, 'confirm_pay.html', {'data': data})
    else:
        customer_email = request.session['uid']
        customer_id = customer_reg.objects.get(email=customer_email)
        bookings = booking.objects.filter(customer=customer_id)
        return render(request, 'booking_status.html', {'bookings':bookings })


def confirm_pay(request):
    if request.method=='POST':
        amount=request.POST['amount']
        bookingid=request.POST['bookingid']

        booking.objects.filter(id=bookingid).update(payment='Completed')

        a=amount
        amount=int(amount)*100

        request.session['amount'] = amount

        request.session['bookingid'] = bookingid


        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

        return render(request, "pay.html", {'r': amount,'a':a})



def success(request):
    bookingid=request.session['bookingid']
    booking.objects.filter(id=bookingid).update(payment='Completed')
    return redirect(booking_status)

def save_rating(request):
    if request.method == "POST":
        b_id = request.POST.get('booking_id')
        score = request.POST.get('score')
        book = booking.objects.get(id=b_id)
        book.rating = score
        book.save()
        return redirect(booking_status)



