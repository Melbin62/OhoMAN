from django.db import models

# Create your models here.
class services(models.Model):
    name=models.CharField(max_length=100)
    image=models.FileField(max_length=50)
    def __str__(self):
        return self.name

class customer_reg(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    phno=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    def __str__(self):
        return self.email

class serviceprov_reg(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    phno=models.CharField(max_length=50)
    # service=models.CharField(max_length=50)
    service=models.ForeignKey(services,on_delete=models.CASCADE)
    baseprice=models.IntegerField()
    servicedetails=models.CharField(max_length=500)
    location=models.CharField(max_length=50)
    license=models.FileField(max_length=50)
    status=models.CharField(max_length=50)
    def __str__(self):
        return self.email



class Login(models.Model):
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    status=models.IntegerField()
    def __str__(self):
        return self.email

class booking(models.Model):
    customer=models.ForeignKey(customer_reg,on_delete=models.CASCADE)
    serviceprov=models.ForeignKey(serviceprov_reg,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.CharField(max_length=50)
    msg=models.CharField(max_length=500)
    status = models.CharField(max_length=50, default='pending')
    payment=models.CharField(max_length=50,default='pending')
    rating = models.IntegerField(default=0, null=True, blank=True)