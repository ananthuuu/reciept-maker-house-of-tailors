from django.db import models

class Receipt(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    invoice_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name
