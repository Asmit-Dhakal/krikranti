from django.db import models


# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Sub_category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    discount_price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='shop/images')
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=10000)
    amount = models.FloatField(default=0)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default='')
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."