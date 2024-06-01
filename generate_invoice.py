import pdfkit
from jinja2 import Environment, FileSystemLoader
from num2words import num2words
import os

def generate_invoice(data, output_pdf):
    # Load the HTML template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('invoice_template.html')

    # Calculate derived fields
    for item in data['items']:
        item['net_amount'] = item['unit_price'] * item['quantity'] - item.get('discount', 0)
        if data['place_of_supply'] == data['place_of_delivery']:
            item['cgst'] = item['net_amount'] * 0.09
            item['sgst'] = item['net_amount'] * 0.09
            item['igst'] = 0
        else:
            item['cgst'] = 0
            item['sgst'] = 0
            item['igst'] = item['net_amount'] * 0.18
        item['total_amount'] = item['net_amount'] + item['cgst'] + item['sgst'] + item['igst']
    
    data['total_amount'] = sum(item['total_amount'] for item in data['items'])
    data['amount_in_words'] = num2words(data['total_amount'], to='currency', lang='en_IN')
    
    # Render the HTML with data
    html_out = template.render(data)

    # Generate PDF with specific path to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(html_out, output_pdf, configuration=config)

# Example data
data = {
    'logo': 'path_to_logo/logo.png',
    'invoice_no': 'KA-310565025-1920',
    'invoice_date': '28.10.2019',
    'order_no': '403-3225714-7676307',
    'order_date': '28.10.2019',
    'seller_name': 'Varasiddhi Silk Exports',
    'seller_address': '75, 3rd Cross, Lalbagh Road',
    'seller_city': 'BENGALURU',
    'seller_state': 'KARNATAKA',
    'seller_pincode': '560027',
    'seller_pan': 'AACFV3325K',
    'seller_gst': '29AACFV3325K1ZY',
    'place_of_supply': 'KARNATAKA',
    'billing_name': 'Madhu B',
    'billing_address': 'Eurofins IT Solutions India Pvt Ltd., 1st Floor, Maruti Platinum, Lakshminarayana Pura, AECS Layou',
    'billing_city': 'BENGALURU',
    'billing_state': 'KARNATAKA',
    'billing_pincode': '560037',
    'billing_state_code': '29',
    'shipping_name': 'Madhu B',
    'shipping_address': 'Eurofins IT Solutions India Pvt Ltd., 1st Floor, Maruti Platinum, Lakshminarayana Pura, AECS Layou',
    'shipping_city': 'BENGALURU',
    'shipping_state': 'KARNATAKA',
    'shipping_pincode': '560037',
    'shipping_state_code': '29',
    'place_of_delivery': 'KARNATAKA',
    'reverse_charge': 'No',
    'items': [
        {
            'description': 'Varasiddhi Silks Men\'s Formal Shirt (SH-05-42, Navy Blue, 42)',
            'unit_price': 338.10,
            'quantity': 1,
            'discount': 0,
        },
        {
            'description': 'Varasiddhi Silks Men\'s Formal Shirt (SH-05-40, Navy Blue, 40)',
            'unit_price': 338.10,
            'quantity': 1,
            'discount': 0,
        },
        {
            'description': 'Shipping Charges',
            'unit_price': 30.96,
            'quantity': 2,
            'discount': 0,
        },
    ],
    'signature': 'path_to_signature/signature.png'
}

# Generate invoice
generate_invoice(data, 'output_invoice.pdf')
