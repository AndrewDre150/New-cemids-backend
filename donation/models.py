from django.db import models

class Donation(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()  
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.full_name} - Donation: ${self.amount:.2f}" 

