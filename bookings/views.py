from django.shortcuts import render
from django.views import View
from .models import Customer,VaccineCenter,QueryCount,QueryTodayCount
from django.contrib import messages
from .forms import CustomerRegistrationForm,CustomerProfileForm,AdminProfileForm,AddVaccineForm,DeleteVaccineForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from datetime import date

# Create your views here.
def home(request):
 return render(request, 'bookings/home.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'bookings/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'bookings/customerregistration.html',{'form':form})

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        if request.user.is_superuser==True:
            return HttpResponseRedirect('/admin-profile/')
        form=CustomerProfileForm()

        d=date.today()
        count=QueryTodayCount.objects.filter(curr_date=d).first()
        if count:
            cnt=count.today_total
        else:
            cnt=0

        return render(request, 'bookings/profile.html',{'form':form,'active':'btn-primary','cnt':cnt})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        d=date.today()
        count=QueryTodayCount.objects.filter(curr_date=d).first()
        if count:
            cnt=count.today_total
        else:
            cnt=0
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            age=form.cleaned_data['age']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,age=age,locality=locality,city=city,zipcode=zipcode,state=state)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
            
        return render(request, 'bookings/profile.html',{'form':form,'active':'btn-primary','cnt':cnt})

@method_decorator(login_required,name='dispatch')
class AdminProfileView(View):

    def get(self,request):
        if request.user.is_superuser==True:
            form=AdminProfileForm(instance=request.user)
            return render(request, 'bookings/admin_profile_view.html',{'form':form,'active':'btn-primary'})
        else:
            return HttpResponseRedirect('/accounts/profile/')
    def post(self,request):
        if request.user.is_superuser==True:
            form=AdminProfileForm(request.POST, instance=request.user)
        else:
            return HttpResponseRedirect('/accounts/profile/')
        if form.is_valid(): 
            usr=request.user
            name=form.cleaned_data['name']
            age=form.cleaned_data['age']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,age=age,locality=locality,city=city,zipcode=zipcode,state=state)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
          
        return render(request, 'bookings/admin_profile_view.html',{'form':form,'active':'btn-primary'})


@login_required
def member(request):
    mem=Customer.objects.filter(user=request.user)
    d=date.today()
    count=QueryTodayCount.objects.filter(curr_date=d).first()
    if count:
        cnt=count.today_total
    else:
        cnt=0

    if len(mem)==0:
        return HttpResponseRedirect('/accounts/profile/')
    return render(request, 'bookings/member.html',{'mem':mem,'active':'btn-primary','cnt':cnt})

@login_required
def bookcenter(request,pk):
    cen=VaccineCenter.objects.all()
    mem=Customer.objects.get(pk=pk)

    d=date.today()
    count=QueryTodayCount.objects.filter(curr_date=d).first()
    if count:
        cnt=count.today_total
    else:
        cnt=0

    if len(cen)==0:
        messages.success(request,'Plaese ask admin to add center')
        return HttpResponseRedirect('/member/')
    else:
        return render(request, 'bookings/bookcenter.html',{'mem':mem,'cen':cen,'prev':pk,'cnt':cnt})

@login_required
def searchcenter(request,prev):
    query=request.GET['search']

    d=date.today()
    count=QueryTodayCount.objects.filter(curr_date=d).first()
    if count:
        cnt=count.today_total
    else:
        cnt=0

    if query:
        cen=VaccineCenter.objects.filter(name__icontains=query)
    else:
        cen=VaccineCenter.objects.all()
    if len(cen)==0:
        messages.success(request,'Plaese ask admin to add center')
        return HttpResponseRedirect('/member/')
    else:
        return render(request, 'bookings/searchcenter.html',{'cen':cen,'prev':prev,'cnt':cnt})



@login_required
def confirmbooking(request,pk,prev):
    cen=VaccineCenter.objects.get(pk=pk)
    mem=Customer.objects.filter(pk=prev).first()
    if not mem:
        messages.success(request,'Already Booked')
        return HttpResponseRedirect('/member/')
    
    d=date.today()
    count=QueryTodayCount.objects.filter(curr_date=d).first()
    if count:
        if count.today_total==10:
            messages.success(request,'Query limit reached for today !! 10')
            return HttpResponseRedirect('/member/')
        count.today_total=count.today_total+1
        count.save()
    else:
        c=QueryTodayCount(curr_date=d,today_total=1)
        c.save()

    mem.delete()
    messages.success(request,'Congratulations!! Booking Confirm')
    return render(request, 'bookings/confirmbooking.html',{'mem':mem,'cen':cen})


@login_required
def add_center(request):
    if request.method == "GET":
        form=AddVaccineForm()
        return render(request, 'bookings/add_vaccine_center.html',{'form':form,'active':'btn-primary'})
    elif request.method == "POST":
        form=AddVaccineForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Center Added Successfully')
            form.save()
        return render(request, 'bookings/add_vaccine_center.html',{'form':form,'active':'btn-primary'})

@login_required
def delete_center(request):
    if request.method == "GET":
        form=DeleteVaccineForm()
        return render(request, 'bookings/delete_vaccine_center.html',{'form':form,'active':'btn-primary'})
    elif request.method == "POST":
        form=DeleteVaccineForm(request.POST)
        if form.is_valid():
            nam=form.cleaned_data['name']
            cen=list(VaccineCenter.objects.values('name'))
            cen=[el['name'] for el in cen]
            # print(cen)
            if nam in cen:
                messages.success(request,'Congratulations!! Center Deleted Successfully')
                d=VaccineCenter.objects.get(pk=nam)
                d.delete()
            else:
                messages.success(request,'Center Not Availabale')
            form.save()
        return render(request, 'bookings/delete_vaccine_center.html',{'form':form,'active':'btn-primary'})
