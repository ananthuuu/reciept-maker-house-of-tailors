from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_receipts, name='list_receipts'),
    path('add/', views.add_receipt, name='add_receipt'),
    path('pdf/<int:receipt_id>/', views.generate_pdf, name='generate_pdf'),
    path('retrieve/<int:receipt_id>/', views.retrieve_receipt, name='retrieve_receipt'),
]
