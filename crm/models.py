from django.db import models

class Customer(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='order', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
