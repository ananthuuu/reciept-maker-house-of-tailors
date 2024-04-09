from django.shortcuts import render, get_object_or_404
from .models import Receipt
from .forms import ReceiptForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def add_receipt(request):
    if request.method == "POST":
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save()
            return generate_pdf(request, receipt.id)
    else:
        form = ReceiptForm()
    return render(request, 'receipts/add_receipt.html', {'form': form})

def generate_pdf(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt_{}.pdf"'.format(receipt_id)

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Dimensions of letter size

    # Define content area
    margin = 72  # 1 inch margin
    content_width = width - 2 * margin
    content_height = 200  # Approximate content height, adjust as needed
    content_start_y = (height / 2) + (content_height / 2) + ((height / 2) + (content_height / 2))/2# Adjust vertical position here

    # Border
    border_padding = 12  # Padding between the border and the content
    p.rect(margin-border_padding, content_start_y - content_height - border_padding,
           content_width + 2*border_padding, content_height + 2*border_padding)

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2.0, content_start_y - 30, "House of Tailors")
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2.0, content_start_y - 45, "Professional Tailoring Services")

    # Separator
    p.line(margin, content_start_y - 60, width - margin, content_start_y - 60)

    # Receipt Details
    p.setFont("Helvetica-Bold", 12)
    details_y = content_start_y - 80  # Starting Y position for details
    details = [
        ("Receipt ID", str(receipt.id)),
        ("Name", receipt.name),
        ("Contact Number", receipt.contact_number),
        ("Invoice Number", receipt.invoice_number),
        ("Amount", "${:,.2f}".format(receipt.amount)),
        ("Reference Number", receipt.reference_number),
    ]

    for label, value in details:
        p.drawString(margin, details_y, f"{label}: {value}")
        details_y -= 18  # Adjust line height as needed

    # Footer
    footer_y = content_start_y - content_height + border_padding
    p.setFont("Helvetica", 10)

    p.showPage()
    p.save()
    return response

def retrieve_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)
    return render(request, 'receipts/receipt_detail.html', {'receipt': receipt})

def list_receipts(request):
    query = request.GET.get('q')
    if query:
        # Search by ID or Name
        receipts_list = Receipt.objects.filter(Q(id__icontains=query) | Q(name__icontains=query))
    else:
        receipts_list = Receipt.objects.all()

    # Pagination
    paginator = Paginator(receipts_list, 10)  # Show 10 receipts per page
    page = request.GET.get('page')
    try:
        receipts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        receipts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        receipts = paginator.page(paginator.num_pages)

    return render(request, 'receipts/list_receipts.html', {'receipts': receipts, 'query': query})