from django import forms
from .models import Receipt

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['name', 'contact_number', 'invoice_number', 'amount', 'reference_number']
